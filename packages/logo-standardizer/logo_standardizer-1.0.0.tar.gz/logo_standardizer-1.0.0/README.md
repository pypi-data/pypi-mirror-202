# logo-standardizer

## Description

A smart logo standardizer that detects both the logo and the background of an unstandardized logo picture and  transforms it into the desired logo standards for app circled or general front-end display.

## Installation

\$ pip install -i logo-standardizer==1.0.0

## Usage

A brief example of how to use the package:

```python
from logo_standardizer import logo_standardize

# call the function directly and fill the required arguments
logo_path = "example/import_dir/img_name" 
export_dir = "example/export_dir"
standard_dimension = 300 # optional

message = logo_standardize.standardize(logo_path, export_dir, standard_dimension)

#print the message to confirm the completion of the process
print(message)
