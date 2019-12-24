# Google Trends Data Summary

This script aggregates data from google trends.

## Usage

```
usage: trends_data.py [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The path to the input file
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The path to the output file
  -v, --verbose         Run in verbose mode
```

the input file is expected to be a newline delimited text file of search terms to query. For example:

input.txt
```
Blockchain
Google
Python
```

```
python trends_data.py -i input.txt -o out.txt
```

will output a csv file (`out.txt`) with the columns:
- Search term
- Global search interest (12/09)
- Global search interest (12/14)
- Global search interest (12/19)
- Most active country
- US search interest (12/09)
- US search interest (12/14)
- US search interest (12/19)
- Most active state

Note that due to weirdness with the google trends API, the global vs US search interest may be a bit inconsistent.

If a search term results in an error (which may occur if there is no data associated with a search term), the error
will be logged to stdout and the row will be outputted with 0 / NA for all columns.

## Python environment

I have included a `requirements.txt` file to set up a virtual environment for this script. To use the virtual
environment run the following commands in a terminal.

```
cd <project directory>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Now you can run the python script.

To exit the virtual environment run:

```
deactivate
```
