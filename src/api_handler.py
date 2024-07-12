import requests
import logging

def post_to_api(api_ip, data):
    url = f'http://{api_ip}:50001/api/v1/preprocessing/'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer testapijson'
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        logging.info(f"API response: {response.text}")
        return response
    except requests.RequestException as e:
        logging.error(f"Failed to post to API: {e}")
        return None
