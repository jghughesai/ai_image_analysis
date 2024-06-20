import requests
import os
from openai import OpenAI, OpenAIError, RateLimitError
import anthropic
import requests
from dotenv import load_dotenv
import json
import openpyxl
import logging
from PIL import Image
from io import BytesIO
import base64

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI()
client2 = anthropic.Anthropic()

def get_ai_response(model, prompt, image):
    if not model:
        raise ValueError("model not provided in get_ai_response")
    if not prompt:
        raise ValueError("prompt not provided in get_ai_response")
    if not image:
        raise ValueError("image not provided in get_ai_response")

    try:
        response = model.get_results(prompt, image)
    except Exception as e:
        logging.error(f"Error calling get_results on {model}: {e}")
        raise

    return response

class GPTInterpreter():
    def __init__(self):
        self.assistant = None
        self.thread = None
        self.file = None

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
            "Authorization": f"Bearer {openai_api_key}"
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
            
    
class ClaudeInterpreter():

    def get_results(self, prompt, image):
        if not prompt:
            raise ValueError("No prompt provided for Claude get_results")
        if not image:
            raise ValueError("No image provided for Claude get_results")
        results = self.analyze_img(prompt, image)
        return results

    def analyze_img(self, prompt, image):
        try:
            if not prompt:
                raise ValueError("No prompt provided to Claude analyze_img")
            if not image:
                raise ValueError("No image provided in Claude analyze_img")
            
            logging.info(f"claude prompt: {prompt}")
            message = client2.messages.create(
                model="claude-3-opus-20240229",
                temperature=0,
                max_tokens=2024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    }
                ],
            )
            text_content = message.content[0].text.strip('```').strip()

            return text_content
        
        except ValueError as e:
            logging.error(f"ValueError in Claude analyze_img: {e}")
            raise
        except anthropic.AnthropicError as e:
            logging.error(f"AnthropicError in Claude analyze_img: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in Claude analyze_img: {e}")
            raise 