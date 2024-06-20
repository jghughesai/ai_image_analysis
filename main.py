import os
import re
from utility import process_image, append_to_file, get_image_id
from prompt_functions import get_prompt_with_example
from api_functions import GPTInterpreter, get_ai_response, RateLimitError
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log")
    ]
)

def process_dir(directory, model_result_path, example_path):
    max_retries = 5
    retry_delay = 60

    filenames = [f for f in os.listdir(directory) if f.endswith(('.png', '.JPG', '.jpeg'))]
    filenames.sort(key=lambda x: int(re.search(r'\d+', x).group()))
    logging.info(f"FILENAMES in directory: {filenames}\n")

    for filename in filenames:
        logging.info(f"\current file being worked: {filename}\n")
        retries = 0

        while retries < max_retries:
            try:
                gpt = GPTInterpreter()

                image = process_image(directory, filename)
                prompt = get_prompt_with_example(example_path)

                gpt_response = get_ai_response(gpt, prompt, image)

                image_id = get_image_id(filename)
                append_to_file(model_result_path, gpt_response, image_id, mode='a')

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

def main():
    try:
        base_directory = "files"
        gpt_result_filename = "gpt_result.tsv"
        example_path = "example_output.csv"

        gpt_result_path = os.path.join(base_directory, gpt_result_filename)

        process_dir(base_directory, gpt_result_path, example_path)
    except Exception as e:
        logging.error(f"An error occurred in main: {e}")
        return

if __name__ == '__main__':
    main()            