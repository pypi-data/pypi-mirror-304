from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info
from PIL import Image
import base64
import io
import torch
import gc
import os
from .utils import create_image_message
import logging

logger = logging.getLogger(__name__)

class OpenZeroxPipeline:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to implement the singleton pattern.
        """
        if cls._instance is None:
            cls._instance = super(OpenZeroxPipeline, cls).__new__(cls)
        return cls._instance

    def __init__(self, 
                 model_name="ashokpoudel/Qwen2-OpenZerox-VL-2B-Instruct-LoRA-FT", 
                 processor_name="Qwen/Qwen2-VL-7B-Instruct", 
                 device="cuda"):
        """
        Initialize with aggressive memory optimization.
        Only run the initialization logic once, even if called multiple times.
        """
        # Check if already initialized to avoid re-initialization
        if hasattr(self, "initialized") and self.initialized:
            return
        
        # Set environment variables for memory efficiency
        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128" 
        
        self.device = device
        
        # Load processor with minimal memory footprint
        self.processor = AutoProcessor.from_pretrained(
            processor_name,
            model_max_length=512,
            padding_side="left",
            truncation_side="left"
        )
        
        # Load model with memory optimizations
        model_kwargs = {
            "device_map": "auto",
            "torch_dtype": torch.float16,
            "low_cpu_mem_usage": True,
            "max_memory": {0: "10GB"},  # Limit GPU memory usage
            "offload_folder": "offload_folder"  # Enable disk offloading
        }
        
        self.model = Qwen2VLForConditionalGeneration.from_pretrained(
            model_name,
            **model_kwargs
        )
        
        # Enable gradient checkpointing if available
        if hasattr(self.model, "gradient_checkpointing_enable"):
            self.model.gradient_checkpointing_enable()
        
        # Optimize model memory usage
        self.model.config.use_cache = False

        # Mark as initialized
        self.initialized = True

    @staticmethod
    def _clear_gpu_memory():
        """
        Aggressively clear GPU memory.
        """
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

    def process_image(self, image_path, max_height=1024):
        """
        Process image with minimal memory footprint.
        """
        try:
            # Create image message
            messages = create_image_message(image_path, max_height)
            return messages
        finally:
            self._clear_gpu_memory()

    @torch.inference_mode()
    def generate_response(self, image_path, max_new_tokens=500):
        """
        Generate response with minimal memory usage.
        """
        try:
            # Process image
            messages = self.process_image(image_path)
            
            # Clear memory after image processing
            self._clear_gpu_memory()
            
            # Process text
            text = self.processor.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
            )
            
            # Process vision info
            image_inputs, video_inputs = process_vision_info(messages)
            
            # Clear intermediate memory
            self._clear_gpu_memory()
            
            # Process inputs with memory optimization
            inputs = self.processor(
                text=[text],
                images=image_inputs,
                videos=video_inputs,
                padding=True,
                return_tensors="pt",
                max_length=512,
                truncation=True
            )
            
            # Move to GPU efficiently
            inputs = {k: v.to(self.device, non_blocking=True) 
                     for k, v in inputs.items() 
                     if isinstance(v, torch.Tensor)}
            
            # Clear CPU memory
            del text, image_inputs, video_inputs
            self._clear_gpu_memory()
            
            # Generate with minimal memory usage
            generated_ids = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=self.processor.tokenizer.pad_token_id,
                eos_token_id=self.processor.tokenizer.eos_token_id,
                use_cache=True, 
                num_beams=1, 
            )
            
            # Process output efficiently
            input_len = inputs["input_ids"].shape[1]
            generated_ids_trimmed = generated_ids[:, input_len:]
            
            # Clear generation memory
            del generated_ids
            self._clear_gpu_memory()
            
            # Decode output
            output_text = self.processor.batch_decode(
                generated_ids_trimmed,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False
            )
            
            return output_text[0] if output_text else ""
            
        finally:
            # Final cleanup
            self._clear_gpu_memory()
    
    def __del__(self):
        """
        Cleanup resources.
        """
        try:
            del self.model
            del self.processor
        except:
            pass
        self._clear_gpu_memory()