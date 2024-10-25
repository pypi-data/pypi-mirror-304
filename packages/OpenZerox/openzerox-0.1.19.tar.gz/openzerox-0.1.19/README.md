# OpenZerox

A Python package for image-based inference using the Qwen2-VL model.

## Installation

```bash
pip install OpenZerox
```

## Usage

```python
from OpenZerox import OpenZeroxPipeline

pipeline = OpenZeroxPipeline()
response = pipeline.generate_response("path/to/your/image.jpg")
print(response)
```