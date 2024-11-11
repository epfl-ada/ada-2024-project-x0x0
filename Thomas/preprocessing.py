from numpy import nan
import pandas as pd

def parse_ratings_file(file_path):
    data = []
    current_review = {}

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # If the line is not empty
                if ': ' in line:  # Check if the line contains the delimiter ': '
                    key, value = line.split(': ', 1)  # Split by the first occurrence of ': '
                    current_review[key] = value
                else:
                    # Handle lines that do not follow the expected key-value format
                    # For example, this could happen for text reviews that span multiple lines
                    if 'text' in current_review:
                        current_review['text'] += ' ' + line  # Append to the 'text' field
                    else:
                        current_review['text'] = line  # Create the 'text' field
            else:  # Blank line indicates the end of a review
                if current_review:  # Ensure that the review is not empty
                    data.append(current_review)
                current_review = {}  # Reset for the next review

        if current_review:  # Catch the last review if there's no trailing blank line
            data.append(current_review)

    # Convert the list of dictionaries to a DataFrame
    return pd.DataFrame(data)


def columns_to_remove(data, value, threshold):
    cols_to_remove = []
    
    for col in data.columns:
        if (data[col] == value).mean() > threshold:
            cols_to_remove.append(col)

    return cols_to_remove


def drop_columns(data, cols_to_remove, save_path):
    data_new = data.drop(columns=cols_to_remove, errors='ignore')
    data_new.to_csv(save_path, index=False)


def main(data_path, sub_folders, remove_vals, new_path):
    
    

if __name__ == "__main__":
    data_path = 'baseData'
    sub_folders = ['BeerAdvocate', 'RateBeer']
    remove_vals = [nan, 0]
    new_path = 'modData'
    
    main(data_path, sub_folders, remove_vals, new_path)

