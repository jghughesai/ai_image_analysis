from setuptools import setup, find_packages

setup(
    name="ai_image_analysis",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pillow",
        "openpyxl",
        "pandas",
        "openai",
        "anthropic",
    ],
    author="Justin Hughes",
    author_email="jghughesai@gmail.com",
    description="A library for AI interpreters and image processing",
    url="https://github.com/jghughesai/ai_image_analysis"
)