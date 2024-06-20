import requests
from .base import BaseInterpreter
from openai import OpenAI, OpenAIError, RateLimitError
import requests
import json
import openpyxl
import logging
from PIL import Image
from io import BytesIO
import base64

class GPTInterpreter(BaseInterpreter):
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI()

    def get_results(self, prompt, image):
        if not prompt:
            raise ValueError("No prompt provided for GPT get_results")
        if not image:
            raise ValueError("No image provided for GPT get_results")
        result = self.analyze_img(prompt, image)
        return result
    
    def analyze_img(self, prompt, image):
        try:
            image_data = base64.b64decode(image)
            images = Image.open(BytesIO(image_data))
            images.verify()
            logging.info("Image successfully verified and decoded from base64.")
        except Exception as e:
            logging.error(f"Error verifying and decoding image from base64: {e}")
        try:
            if not prompt:
                raise ValueError("No prompt provided in GPT analyze_img")
            if not image:
                raise ValueError("No image provided in GPT analyze_img")
            logging.info(f"gpt prompt: {prompt}")
            headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
            }

            payload = {
            "model": "gpt-4o",
            "messages": [
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": prompt
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image}"
                    }
                    }
                ]
                }
            ],
            "temperature": 0,
            "max_tokens": 3000
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            response_content = response.content.decode('utf-8')

            if response.status_code != 200:
                raise OpenAIError(f"Request failed with status {response.status_code}: {response_content}")

            response_json = json.loads(response_content)

            if "choices" not in response_json:
                raise KeyError(f"'choices' not found in response: {response_json}") 
            text_content = response_json['choices'][0]['message']['content']
            text_content = text_content.strip('```').strip()

            return text_content
        except RateLimitError as e:
            logging.error(f"OpenAI RateLimitError in GPT analyze_img: {e}. Retrying...")
            raise
        except ValueError as e:
            logging.error(f"ValueError in GPT analyze_img: {e}")
            raise
        except OpenAIError as e:
            logging.error(f"OpenAIError in GPT analyze_img: {e}")
            raise
        except KeyError as e:
            logging.error(f"KeyError in GPT analyze_img: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in GPT analyze_img: {e}")
            raise