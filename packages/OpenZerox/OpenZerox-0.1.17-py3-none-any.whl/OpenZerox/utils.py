from PIL import Image
import base64
import io
import os

def create_image_message(image_path, max_height=1024):
    """
    Create a message containing the image encoded in base64 format.
    
    Parameters:
    - image_path: Path to the image file.
    - max_height: Maximum height to resize the image while maintaining aspect ratio.
    
    Returns:
    - A list containing the message structure with the base64 encoded image.
    """
    # Open the image and convert to RGB
    with Image.open(image_path) as image:
        # Resize image while maintaining aspect ratio
        aspect_ratio = image.width / image.height
        new_width = int(max_height * aspect_ratio)
        resized_image = image.resize((new_width, max_height), Image.ANTIALIAS)
        
        # Encode the image to base64
        buffered = io.BytesIO()
        
        # Determine the format based on the original image format
        if image.format in ['JPEG', 'JPG']:
            format_to_use = "JPEG"
        else:
            format_to_use = "PNG"  # Fallback to PNG for other formats
            
        resized_image.save(buffered, format=format_to_use)
        
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Create the message structure
        messages = [{
            "role": "user",
            "content": [{
                "type": "image",
                "image": f"data:image/{format_to_use.lower()};base64,{img_str}",
            }],
        }]
        
        return messages
