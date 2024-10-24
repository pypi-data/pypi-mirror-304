from OpenZerox import OpenZeroxPipeline

# Initialize the pipeline
pipeline = OpenZeroxPipeline()

# Path to the image file
image_path = "path/to/your/image.png"

# Generate a response based on the image
response = pipeline.generate_response(image_path)
print(response)
