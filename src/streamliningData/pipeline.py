import papermill as pm
import logging

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
