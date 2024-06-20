import os
import pandas as pd
import base64
import csv
import openpyxl
import logging
import io

def process_image(dir: str, filename: str):
    logging.info(f"filename in process_image: {filename}")
    try:
        image_path = f"{dir}/{filename}"
        with open(image_path, 'rb') as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            logging.info(f"Base64 image string (start): {base64_image[:100]}")
            logging.info(f"Base64 image string (end): {base64_image[-100:]}")
        return base64_image
    except Exception as e:
        logging.error(f"Error processing image {filename}: {e}")
        raise

def get_example_content(file_path: str):
    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"example file not found at: {file_path}")
        
        example_df = pd.read_csv(file_path, delimiter=';', on_bad_lines='skip')
        example_df_str = example_df.to_csv(index=False, sep=';')
        return example_df_str
    except FileNotFoundError as fnf_error:
        logging.error(fnf_error)
        raise
    except pd.errors.EmptyDataError:
        logging.error(f"No data in file at: {file_path}")
        raise
    except pd.errors.ParserError as pe:
        logging.error(f"Parsing error in file at: {file_path}: {pe}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in get_example_content: {e}")
        raise

def append_to_file(file_path: str, data: str, new_column_value: str, mode='w'):
    try:
        data_io = io.StringIO(data.strip())
        csv_reader = csv.reader(data_io, delimiter='|')

        with open(file_path, mode, newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter='|')

            for row in csv_reader:
                new_row = [new_column_value] + row
                csv_writer.writerow(new_row)
        logging.info(f"Data successfully saved to {file_path}")
    except Exception as e:
        logging.error(f"Error writing to file {file_path}: {e}")
        raise

def get_image_id(filename: str):
    try:
        if filename.endswith(('.JPG', '.JPEG', '.jpg', '.jpeg')):
            img_id = filename.rsplit('.', 1)[0]
        else:
            img_id = filename
        return img_id
    except Exception as e:
        logging.error(f"Unexpected error getting img id, {e}")
        raise