# twitter-poc
This twitter-poc application is split into two parts:

1. `auth.py` - This script is used to authenticate the user and store the access token locally.
2. `like.py` - This script is used to like the tweet by providing tweet id.

Developer needs to run above scripts separately in order to authenticate the user and like the tweet.

### Prerequisites

- Python 3.11
- pip (Python package installer)
- A Twitter Developer account with API credentials

### Setup

1. Download the repository:
    ```sh
    Downlaod zip file and extract it in your local machine
    cd twitter-poc
    ```

2. Create a virtual environment:
    ```sh
    python -m venv .venv
    ```

3. Activate the virtual environment:

    - On macOS/Linux:
        ```sh
        source .venv/bin/activate
        ```

4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

5. Create a `.env` file in the root directory and add your Twitter API credentials use `example.env` as a template:
    ```env
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    ```

### Running the Application

1. Authenticate the user:
    ```sh
    python auth.py
    ```
2. Like the tweet by providing tweet id:
    ```sh
    python like.py
   ```

