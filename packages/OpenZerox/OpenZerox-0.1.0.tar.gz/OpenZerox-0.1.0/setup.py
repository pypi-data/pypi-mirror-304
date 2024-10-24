from setuptools import setup, find_packages

setup(
    name="OpenZerox",
    version="0.1.0",
    author="Your Name",
    description="A wrapper for the Qwen2-VL model for image-based inference.",
    packages=find_packages(),
    install_requires=[
        "torch",
        "transformers",
        "Pillow",
        "qwen-vl-utils"
    ],
    python_requires='>=3.8',
)
