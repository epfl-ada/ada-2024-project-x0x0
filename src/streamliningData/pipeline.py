import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def run_notebook(path):
    with open(path) as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': './'}})

# List your notebook files here
notebooks = [
    'notebook1.ipynb',
    'notebook2.ipynb',
    'notebook3.ipynb'
]

for notebook in notebooks:
    print(f"Running {notebook}...")
    run_notebook(notebook)  # Call run_notebook with each notebook path
    print(f"Finished {notebook}")
