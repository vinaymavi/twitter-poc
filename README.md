# twitter-poc
This project contains twitter AI POC.

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

1. Start the FastAPI server:
    ```sh
    python app.py
    ```
 
When this script runs first time it will ask for user authorization to access twitter account and store the access token locally.

Run this script again to like the tweet by providing tweet id.

