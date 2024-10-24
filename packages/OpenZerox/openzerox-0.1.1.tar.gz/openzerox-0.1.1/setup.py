from setuptools import setup, find_packages

setup(
    name="OpenZerox",
    version="0.1.1",
    author="Ashok Poudel",                   
    author_email="ashok.poudel@gmail.com",
    description="A wrapper for the Qwen2-VL model based for image-based inference to convert pdf image to markdown.",
    packages=find_packages(),
    install_requires=[
        "torch",
        "transformers",
        "Pillow",
        "qwen-vl-utils"
    ],
    python_requires='>=3.8',
    classifiers=[                         
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)