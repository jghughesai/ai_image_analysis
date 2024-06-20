import os
import pandas as pd
import openpyxl
import logging

def get_example_content(file_path):
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

def get_prompt_with_example(example_path):
    try:
        if not example_path:
            raise ValueError("example_path is not provided")
        
        example = get_example_content(example_path)

        if example is None:
            raise ValueError(f"Failed to get example content from {example_path}")
        
        prompt = f"""
System Prompt for Analyzing Handwritten Bill of Materials (BoM):

Objective: To accurately extract and digitize information from handwritten Bill of Materials (BoM) images.

Tasks:

Text Recognition:

Identify and extract all handwritten text from the provided image.

Ensure the accuracy of recognized text, focusing on numbers, letters, and special characters.

Categorization:

Categorize the extracted text into appropriate fields based on the BoM structure, such as:

Item Type (e.g., Ball Bearings, Belts, Cam Follower Bushings, Chain, Clamps)

Specific Item Description (e.g., Metal, Ball, Flange, Pillow Block, Radial Paper, etc.)

Item Codes (e.g., 01-001-000, 1-045-000, etc.)

Validation:

Cross-check the extracted data for any inconsistencies or illegible entries.

Highlight areas where the handwriting is unclear or ambiguous for further review.

Output Format:

Present the extracted and categorized data in a structured format such as a table or a spreadsheet.

Ensure each item is clearly associated with its respective category and code.

Error Handling:

If any part of the text is not recognizable, indicate this in the output with a placeholder (e.g., [Unclear]).

The following are snippets of various example formats for you to use in formatting your output. These examples are provided to assist in recognizing different possible layouts that may represent the Bill of Materials image I provided you with. Please note that the format of the current BOM image may not directly match any of these examples so make sure to look very closely at the image and make sure your output is accurate:

{example}


Instructions for the AI System:

Pay special attention to the format and spacing of handwritten text to correctly interpret and categorize the information.

Present the final output in a user-friendly and editable format, ensuring easy access for review and modification.
        
Instructions with specifics:

Please extract the data from the handwritten bill of materials image and present it in a structured table format. Identify the column headers and populate the corresponding data accurately. If any information is unclear or illegible, indicate that in the respective cell. Make the table tab delimited ('|') and add a new-line character ('\\n') to end of each row.

The table should include the following columns if present in the image:

- Category
- Subcategory
- Part Number or ID
- Description or Name
- Material or Specification
- Dimensions or Size
- Quantity or Count
- Any additional columns present in the image

If a column is missing from the image and/or the example, you can omit it from the table. Sometimes the Part Number doesn't follow sequential ordering so it is very important that you examine each Part Number on every row to ensure accuracy. Please ensure the data is captured accurately and in the correct format.

Do not include any comments or other text in the output, just output the table.
"""
        return prompt
    
    except Exception as e:
        logging.error(f"Error in get_initial_prompt: {e}")
        raise