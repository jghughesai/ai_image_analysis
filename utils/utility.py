import os
import pandas as pd
import base64
import csv
import openpyxl
import logging
import io

def process_image(dir, filename):
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

def append_to_file(file_path, data, new_column_value, mode='w'):
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

def get_image_id(filename):
    try:
        if filename.endswith(('.JPG', '.JPEG', '.jpg', '.jpeg')):
            img_id = filename.rsplit('.', 1)[0]
        else:
            img_id = filename
        return img_id
    except Exception as e:
        logging.error(f"Unexpected error getting img id, {e}")
        raise