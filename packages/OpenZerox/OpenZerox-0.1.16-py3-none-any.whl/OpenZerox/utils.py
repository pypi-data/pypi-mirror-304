from PIL import Image
import base64
import io
import torch

def resize_image(image, max_height=1024):
    """
    Resize the image while maintaining aspect ratio.
    """
    aspect_ratio = image.width / image.height
    new_width = int(max_height * aspect_ratio)
    image.thumbnail((new_width, max_height))
    return image

def encode_image_to_base64(image, format="PNG"):
    """
    Convert the image to a base64-encoded string.
    """
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str

def create_image_message(image_path, max_height=1024):
    """
    Process an image and create a message dictionary suitable for model input.
    """
    # Open and resize the image
    with Image.open(image_path).convert('RGB') as image:
        resized_image = resize_image(image, max_height)
        img_str = encode_image_to_base64(resized_image)
        
        # Create the message structure expected by the model
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": f"data:image/png;base64,{img_str}",
                    }
                ]
            }
        ]
        return messages
