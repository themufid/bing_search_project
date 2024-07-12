import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

def download_cache(url, destination):
    try:
        headers = {
            'User-Agent': load_env_variables('env/headers.env').get('USER_AGENT', 'Your_User_Agent_String_Here'),
            'Accept-Language': 'en-US,en;q=0.5',
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        with open(destination, 'wb') as f:
            f.write(response.content)
        
        logging.info(f"Downloaded cache from {url} to {destination}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading cache: {str(e)}")

def main():
    url = 'https://website.com/cache_file.zip'
    destination = 'path/to/save/cache_file.zip'
    download_cache(url, destination)

if __name__ == "__main__":
    main()
