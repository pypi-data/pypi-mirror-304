from PIL import Image
import io
import base64

def resize_image(image, max_height=1024):
    """
    Resize the image while maintaining the aspect ratio.
    
    :param image: PIL Image object.
    :param max_height: Maximum height of the resized image.
    :return: Resized image.
    """
    aspect_ratio = image.width / image.height
    new_width = int(max_height * aspect_ratio)
    image.thumbnail((new_width, max_height))
    return image

def encode_image_to_base64(image):
    """
    Convert the image to a base64 string.
    
    :param image: PIL Image object.
    :return: Base64 encoded string of the image.
    """
    buffered = io.BytesIO()
    return base64.b64encode(buffered.getvalue()).decode('utf-8')
