import papermill as pm
import logging
import os

def verify_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file does not exist: {file_path}")
        print("Stopping the execution.")
        exit()  # Stop the script execution if file does not exist
    else:
        print(f"The file exists: {file_path}")

def verify_and_create_directory(directory_path):
    if not os.path.exists(directory_path):
        print(f"The directory does not exist: {directory_path}")
        print(f"Creating the directory: {directory_path}")
        os.makedirs(directory_path)  # Create the directory (and parents if needed)
    else:
        print(f"The directory already exists: {directory_path}")

#I found this logger code online in github issue post, it works to suppress what I want
class PapermillFilter(logging.Filter):
    def filter(self, record):
        #suppress these annoying console logs
        return not ('Executing Cell' in record.getMessage() or 'Ending Cell' in record.getMessage())

# Apply the custom filter to papermill's logger
logger = logging.getLogger('papermill')
logger.setLevel(logging.INFO)  #Info level will show ipynb prints
handler = logging.StreamHandler()
handler.addFilter(PapermillFilter())  # Apply our filter
logger.addHandler(handler)

# List your notebook files here
notebook_paths = [
    'src/streamliningData/reducing_csv.ipynb',
    'src/streamliningData/BA_reducing_txt.ipynb',
    'src/streamliningData/RB_reducing_txt.ipynb',
    'src/streamliningData/BA_extra_cols.ipynb',
    'src/streamliningData/RB_extra_cols.ipynb',
    'src/streamliningData/BA_US_data.ipynb',
    'src/streamliningData/RB_US_data.ipynb'
    
    #add extract_php.ipynb
]


files_to_check = [
    'baseData/BeerAdvocate/beers.csv',
    'baseData/BeerAdvocate/breweries.csv',
    'baseData/BeerAdvocate/ratings.txt',
    'baseData/BeerAdvocate/reviews.txt',
    'baseData/BeerAdvocate/users.csv',
    'baseData/RateBeer/beers.csv',
    'baseData/RateBeer/breweries.csv',
    'baseData/RateBeer/ratings.txt',
    'baseData/RateBeer/reviews.txt',
    'baseData/RateBeer/users.csv',
]

directories_to_check = [
    'additionalData',
    'minimizedData',
    'USData',
]

for file in files_to_check:
    verify_file_exists(file)

for directory in directories_to_check:
    verify_and_create_directory(directory)

for directory in directories_to_check:
    if not os.path.exists(directory):
        print(f"Warning: Directory '{directory}' does not exist.")
    else:
        print(f"Directory '{directory}' exists.")

print('\nIt takes around 12 minutes to run everything \n')

for notebook in notebook_paths:
    pm.execute_notebook(
        notebook,
        notebook, #dont want to make new file
        log_output=True,
        progress_bar=False,
        report_mode=True
    )
    print(f"Finished {notebook}")
    
print('Finished all notebooks! Congrats, you now have the right data!')
