from .base import BaseInterpreter
import anthropic
import openpyxl
import logging

class ClaudeInterpreter(BaseInterpreter):
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = anthropic.Anthropic()

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
            message = self.client.messages.create(
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