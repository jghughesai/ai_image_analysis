import logging
from interpreters.base import BaseInterpreter

def analyze_image(interpreter: BaseInterpreter, prompt: str, base64_image):
    if not interpreter:
        raise ValueError("interpreter not provided in get_ai_response")
    if not prompt:
        raise ValueError("prompt not provided in get_ai_response")
    if not base64_image:
        raise ValueError("base64_image not provided in get_ai_response")

    try:
        response = interpreter.get_results(prompt, base64_image)
    except Exception as e:
        logging.error(f"Error calling get_results on {interpreter}: {e}")
        raise

    return response