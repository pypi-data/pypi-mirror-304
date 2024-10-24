from ._core import _perform_ocr

def TwiMethod(image_path):
    """
    Perform OCR on the given image file.
    
    Parameters:
    - image_path (str): The path to the image file.
    
    Returns:
    - str: The extracted text or an error message.
    """
    return _perform_ocr(image_path)
