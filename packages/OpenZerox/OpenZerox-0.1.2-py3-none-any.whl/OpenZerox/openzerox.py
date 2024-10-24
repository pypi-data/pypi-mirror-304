from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info
from PIL import Image
import base64
import io
import torch

class OpenZeroxPipeline:
    def __init__(self, model_name="ashokpoudel/Qwen2-OpenZerox-VL-2B-Instruct-LoRA-FT", processor_name="Qwen/Qwen2-VL-7B-Instruct", device="cuda"):
        """
        Initialize the model and processor.
        
        :param model_name: The name of the model to load.
        :param processor_name: The name of the processor to use.
        :param device: The device to use ('cuda' or 'cpu').
        """
        self.model = Qwen2VLForConditionalGeneration.from_pretrained(
            model_name, torch_dtype="auto", device_map="auto"
        )
        self.processor = AutoProcessor.from_pretrained(processor_name)
        self.device = device

    def process_image(self, image_path):
        """
        Load and process an image for inference.
        
        :param image_path: Path to the image file.
        :return: A dictionary with processed messages.
        """
        with open(image_path, "rb") as image_file:
            image = Image.open(image_file)

            # Resize the image while maintaining aspect ratio with max height 1024
            max_height = 1024
            aspect_ratio = image.width / image.height
            new_width = int(max_height * aspect_ratio)
            image.thumbnail((new_width, max_height))

            # Convert the image to base64
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

            # Create the messages variable
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "image": "data:image/png;base64," + img_str,
                        },
                    ],
                }
            ]

        return messages

    def generate_response(self, image_path, max_new_tokens=1000):
        """
        Generate a response for the provided image.
        
        :param image_path: Path to the image file.
        :param max_new_tokens: Maximum tokens to generate.
        :return: Generated text response.
        """
        # Process the image and prepare the input for the model
        messages = self.process_image(image_path)
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to(self.device)
        
        # Inference: Generation of the output
        generated_ids = self.model.generate(**inputs, max_new_tokens=max_new_tokens)
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = self.processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        
        return output_text
