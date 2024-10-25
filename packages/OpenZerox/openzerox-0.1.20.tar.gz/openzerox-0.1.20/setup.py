from setuptools import setup, find_packages

setup(
    name="OpenZerox",
    version="0.1.20",
    author="Ashok Poudel",                   
    author_email="ashok.poudel@gmail.com",
    description="A wrapper for the Qwen2-VL model based for image-based inference to convert pdf image to markdown.",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.45.2",  # Qwen2 requires newer transformers
        "Pillow",
        "qwen-vl-utils",
        "accelerate>=0.21.0",    # Required for model loading
        "qwen-vl-utils>=0.0.8"
    ],
    python_requires='>=3.8',
    classifiers=[                         
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)