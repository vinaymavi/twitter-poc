import os
import json
import tweepy
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
# Load environment variables from .env file
load_dotenv()

# Load Twitter API credentials from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_FILE = "access_token.json"

def load_access_token():
    """ Load token from file """
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None


if __name__ == "__main__":
    logging.info( "Starting Twitter OAuth2.0 PKCE flow")
    logging.info( "Checking for existing access token")
    token_data = load_access_token()

    if not token_data:
        logging.info("No access token found. Run auth.py to generate access token")
    else:
        logging.info("Access token found. Fetching user details")
        client = tweepy.Client(bearer_token=token_data["access_token"], access_token=token_data['access_token'], consumer_key=CLIENT_ID, consumer_secret=CLIENT_SECRET)
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