import requests
from user_agent import generate_user_agent

def _perform_ocr(image_path, api_key='3699294be288957', language='eng', overlay=False):
    try:
        payload = {
            'isOverlayRequired': overlay,
            'apikey': api_key,
            'language': language,
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
                'https://api.ocr.space/parse/image',
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
