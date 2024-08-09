import os
from ..interpreters.base import BaseInterpreter
import re
from ..utils.utility import process_image, append_to_file, get_image_id
from ..interpreters.gpt_interpreter import RateLimitError
from ..utils.ai_functions import analyze_image
import logging
import time
import pandas as pd
import io
import importlib.util

def load_prompt_from_subdir(sub_dir_path):
    prompt_path = os.path.join(sub_dir_path, 'prompt.py')
    spec = importlib.util.spec_from_file_location("prompt", prompt_path)
    prompt_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prompt_module)
    return prompt_module.prompt

def process_all_formats(interpreter: BaseInterpreter, base_directory: str, output_path: str):
    format_dataframes = {}

    # Process each format subdirectory
    for format_dir in os.listdir(base_directory):
        format_path = os.path.join(base_directory, format_dir)
        if not os.path.isdir(format_path):
            continue

        format_df = process_format(interpreter, format_path)
        format_dataframes[format_dir] = format_df

    # Combine all DataFrames
    combined_df = pd.concat(format_dataframes.values(), keys=format_dataframes.keys())
    combined_df = combined_df.reset_index(level=0).rename(columns={'level_0': 'Format'})

    # Write combined DataFrame to TSV
    combined_df.to_csv(output_path, sep='\t', index=False)
    logging.info(f"Combined data from all formats written to: {output_path}")

def process_format(interpreter: BaseInterpreter, directory: str):
    format_df = pd.DataFrame()
    prompt = load_prompt_from_subdir(directory)

    filenames = [f for f in os.listdir(directory) if f.endswith(('.png', '.JPG', '.jpeg'))]
    filenames.sort(key=lambda x: int(re.search(r'\d+', x).group()))

    for filename in filenames:
        try:
            image = process_image(directory, filename)
            gpt_response = analyze_image(interpreter, prompt, image)
            image_id = get_image_id(filename)
            
            response_df = pd.read_csv(io.StringIO(gpt_response), sep='|')
            response_df.insert(0, 'Image ID', image_id)
            
            format_df = pd.concat([format_df, response_df], ignore_index=True)
        except Exception as e:
            logging.error(f"Error processing {filename} in {directory}: {e}")

    return format_df