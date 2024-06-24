import os
from ..interpreters.base import BaseInterpreter
import re
from ..utils.utility import process_image, append_to_file, get_image_id
from ..interpreters.gpt_interpreter import RateLimitError
from ..utils.ai_functions import analyze_image
import logging
import time

def process_dir(interpreter: BaseInterpreter, directory: str, prompt: str, output_path: str):
    max_retries = 5
    retry_delay = 60

    # Sort filenames in numerical ascending order
    filenames = [f for f in os.listdir(directory) if f.endswith(('.png', '.JPG', '.jpeg'))]
    filenames.sort(key=lambda x: int(re.search(r'\d+', x).group()))
    logging.info(f"FILENAMES in directory: {filenames}\n")

    # Works each image file in provided dir
    for filename in filenames:
        logging.info(f"\current file being worked: {filename}\n")
        retries = 0

        while retries < max_retries:
            try:
                # Process image and return base64 image for passing to ai vision model
                image = process_image(directory, filename)

                gpt_response = analyze_image(interpreter, prompt, image)

                # Retrieves filename without ext for creating 'Image ID' column
                image_id = get_image_id(filename)

                # Appends current iteration's gpt response to file specified as 'output_path'
                append_to_file(output_path, gpt_response, image_id, mode='a')

                logging.info(f"gpt_response: {gpt_response}")

                break

            except RateLimitError as e:
                retries +=1
                logging.error(f"OpenAI RateLimitError in GPT analyze_img: {e}. Retrying...")
                time.sleep(retry_delay)
            except Exception as e:
                logging.error(f"An error occurred in process_dir: {e}")
                break

    logging.info(f"\nCompleted audit for {directory} written as tsv file\n")