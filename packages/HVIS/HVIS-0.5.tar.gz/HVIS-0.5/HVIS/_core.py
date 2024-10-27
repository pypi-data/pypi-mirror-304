import requests
from user_agent import generate_user_agent
import base64

class twiMethod:
    def __init__(self, api_key=None, language='eng', overlay=False):
        self.api_key = api_key or base64.b64decode('MzY5OTI5NGJlMjg4OTU3'.encode('utf-8')).decode('utf-8')
        self.language = language
        self.overlay = overlay
        self.api_url = base64.b64decode('aHR0cHM6Ly9hcGkub2NyLnNwYWNlL3BhcnNlL2ltYWdl'.encode('utf-8')).decode('utf-8')

    def scan(self, image_path):
        try:
            payload = {
                'isOverlayRequired': self.overlay,
                'apikey': self.api_key,
                'language': self.language,
            }
            
            try:
                with open(image_path, 'rb') as f:
                    image_data = f.read()
            except FileNotFoundError:
                return f"Error: The file '{image_path}' was not found. Please check the path and try again."
            except IOError:
                return f"Error: Unable to read the file '{image_path}'. Please ensure the file is accessible."
            
            try:
                response = requests.post(
                    self.api_url,
                    files={image_path: image_data},
                    data=payload,
                    headers={'User-Agent': generate_user_agent()}
                )
                response.raise_for_status()
            except requests.exceptions.HTTPError as http_err:
                return f"HTTP error occurred: {http_err}"
            except requests.exceptions.ConnectionError:
                return "Error: Unable to connect to the OCR service. Please check your internet connection."
            except requests.exceptions.Timeout:
                return "Error: The request timed out. Please try again later."
            except requests.exceptions.RequestException as req_err:
                return f"An error occurred while making the request: {req_err}"

            try:
                return response.json()['ParsedResults'][0]['ParsedText']
            except (KeyError, IndexError) as e:
                return f"Error: Unable to extract text from the response. The response structure might have changed: {e}"
            except ValueError:
                return "Error: Unable to parse JSON response. The OCR API might have returned an unexpected response."
            
        except Exception as e:
            return f"An unexpected error occurred: {e}"
