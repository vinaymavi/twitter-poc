import os
import json
import tweepy
import webbrowser
from fastapi import FastAPI, Request
from threading import Thread
import uvicorn
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
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
    logging.info(f"Saving access token to file {TOKEN_FILE}")
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
        logging.warning("Authorization failed no auth code received")
        return {"error": "Authorization failed no auth code received"}
    logging.info("Fetching access token...")
    access_token = auth.fetch_token(str(request.url))
    logging.info("Access token received")
    if access_token:
        save_access_token(access_token)
        logging.info("Access token saved to file")
        logging.info("Authorization successful! Kill this process and run the app again to like the tweet")
        return {"message": "Authorization successful! You can close this window."}
    return {"error": "Authorization failed"}

def start_fastapi_server():
    """ Runs FastAPI server in a thread """
    logging.info("\nStarting FastAPI server to capture callback...")
    thread = Thread(target=uvicorn.run, args=(app,), kwargs={"host": "127.0.0.1", "port": 8000})
    thread.start()
    thread.join()

if __name__ == "__main__":
    logging.info( "Starting Twitter OAuth2.0 PKCE flow")
    logging.info( "Checking for existing access token")
    token_data = load_access_token()

    if not token_data:
        logging.info("No access token found. Generating authorization URL")
        auth_url = auth.get_authorization_url()
        webbrowser.open(auth_url)
        logging.info(f"Open this URL in your browser if it doesn't open automatically: {auth_url}")
        start_fastapi_server()
    else:
        logging.info("Access token found. Fetching user details")
        client = tweepy.Client(bearer_token=token_data["access_token"], access_token=token_data['access_token'], consumer_key=CLIENT_ID, consumer_secret=CLIENT_SECRET)
        # passing user_auth=False as using OAuth2.0 PKCE flow
        user = client.get_me(user_auth=False)
        user_id = user.data.id
        logging.info(f"User ID: {user_id}")
        while True:
            tweet_id = input("\nEnter the Tweet ID to like (or 'exit' to quit): ").strip()
            if tweet_id.lower() == "exit":
                break
            try:
                # passing user_auth=False as using OAuth2.0 PKCE flow
                response = client.like(tweet_id, user_auth=False)
            except tweepy.TooManyRequests as e:
                logging.warning("Rate limit exceeded. Please try again later.")
                continue
            except tweepy.Unauthorized as e:
                logging.warning("Unauthorized access. Please check your credentials.")
                continue
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                continue

            logging.info(f"Tweet liked successfully! Tweet ID: {tweet_id}")