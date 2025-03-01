import os
import json
import tweepy
import webbrowser
from fastapi import FastAPI, Request
from threading import Thread
import uvicorn
from dotenv import load_dotenv
from starlette.responses import RedirectResponse

# Allow insecure transport for development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Load environment variables from .env file
load_dotenv()

# Load Twitter API credentials from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"
TOKEN_FILE = "access_token.json"
SCOPES = ["tweet.read", "tweet.write", "like.read", "like.write", "offline.access","users.read"]

auth = tweepy.OAuth2UserHandler(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPES)

app = FastAPI()


def save_access_token(token_data):
    """ Save token to file """
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)

def load_access_token():
    """ Load token from file """
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None

@app.get("/callback")
async def callback(request: Request):
    """ Handle Twitter OAuth callback """
    auth_code = request.query_params.get("code")
    response_state = request.query_params.get("state")

    if not auth_code:
        return {"error": "Authorization failed or state mismatch"}

    access_token = auth.fetch_token(str(request.url))
    if access_token:
        save_access_token(access_token)
        return {"message": "Authorization successful! You can close this window."}
    return {"error": "Authorization failed"}

def start_fastapi_server():
    """ Runs FastAPI server in a thread """
    thread = Thread(target=uvicorn.run, args=(app,), kwargs={"host": "127.0.0.1", "port": 8000})
    thread.start()
    thread.join()

if __name__ == "__main__":
    token_data = load_access_token()

    if not token_data:
        print("No access token found. Generating authorization URL")
        auth_url = auth.get_authorization_url()
        webbrowser.open(auth_url)
        print(f"Open this URL in your browser if it doesn't open automatically: {auth_url}")
        print("\nStarting FastAPI server to capture callback...")
        start_fastapi_server()
    else:
        client = tweepy.Client(bearer_token=token_data["access_token"], access_token=token_data['access_token'], consumer_key=CLIENT_ID, consumer_secret=CLIENT_SECRET)
        user = client.get_me(user_auth=False)
        user_id = user.data.id

        while True:
            tweet_id = input("\nEnter the Tweet ID to like (or 'exit' to quit): ").strip()
            if tweet_id.lower() == "exit":
                break
            try:
                response = client.like(tweet_id, user_auth=False)
            except tweepy.TooManyRequests as e:
                print("Rate limit exceeded. Please try again later.")
                continue
            except tweepy.Unauthorized as e:
                print("Unauthorized access. Please check your credentials.")
                continue
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

            print(response)