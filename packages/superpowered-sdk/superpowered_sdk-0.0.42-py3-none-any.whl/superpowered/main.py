import requests
import base64
import os

# initialize variables
BASE_URL = 'https://api.superpowered.ai/v1/'

def init(api_key_id: str, api_key_secret: str, verbose: bool = False):
    """
    init is used to set the API key for the SDK. It should be called before any other SDK functions are called.
    """
    token = base64.b64encode((f'{api_key_id}:{api_key_secret}').encode('utf-8')).decode('utf-8')
    os.environ['SUPERPOWERED_API_KEY'] = token

def get_headers():
    token = os.environ['SUPERPOWERED_API_KEY']
    HEADERS = {'Authorization': f'Bearer {token}'}
    return HEADERS

# exceptions
class NoApiKeyError(Exception):
    def __init__(self):
        super().__init__('No API key has been set. Please run check that your API key is correct and then run `superpowered.init(api_key)` before continuing')

def _format_http_response(resp: requests.Response):
    if resp.status_code != 200:
        if resp.status_code == 204:
            return {
                'http_code': resp.status_code,
                'body': None
            }
        else:
            #print ("Error:", resp.status_code)
            raise Exception(resp.status_code, resp.json())
    return {
        'http_code': resp.status_code,
        'body': resp.json()
    }