# -*- coding: utf-8 -*-
"""prescription-parser.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iM_bwQG539HiaJF_XvLDHxy6nM5866YZ

### Data Input
Upload file with text.
"""

from google.colab import files
uploaded = files.upload()

"""### Install Pre-requisites
- tesseract linux binary
- pytesseract
"""

!sudo apt install tesseract-ocr -y

!pip install pytesseract

"""### OCR"""

import pytesseract
from PIL import Image
file_content = pytesseract.image_to_string(Image.open('test1.jpg'))

"""### Post-processing to Excel"""

# Run this cell only once
from collections import OrderedDict
if 'final_prescriptions' not in locals():
  final_prescriptions = OrderedDict()

def parse_prescription(file_content):
  file_content_str = [elem.strip() for elem in file_content.split('\n')]
  prescription_row = {}
  for elem in map(str,file_content_str):
    if ':' in elem:
      key, val = elem.split(':')
      prescription_row[key] = val
  return prescription_row

# file_content = open('out.txt.txt', 'rb').readlines()
prescription_row=parse_prescription(file_content)

final_prescriptions[len(final_prescriptions)] = prescription_row

import pandas as pd
df = pd.DataFrame.from_dict(final_prescriptions, orient="index")

#Export to Google Sheets / Part 1 Auth
!pip install --upgrade --quiet gspread
from google.colab import auth
auth.authenticate_user()

import gspread
from oauth2client.client import GoogleCredentials

gc = gspread.authorize(GoogleCredentials.get_application_default())

#Export to Google Sheets / Part 2 Export
from gspread_dataframe import get_as_dataframe, set_with_dataframe

patient_data = gc.open_by_url('https://docs.google.com/spreadsheets/d/1tbLYRSAfDMbr8cueQInhWVA6ISAD2c8kc9X7EonvOX8/edit#gid=0')
ws1 = patient_data.get_worksheet(0)
ws1.update_cell(2,2,df.iloc[0]['Name'])
ws1.update_cell(2,3,df.iloc[0]['Zip'])
ws1.update_cell(2,4,df.iloc[0]['ePharmacy'])
ws1.update_cell(2,5,df.iloc[0]['Mail'])
ws1.update_cell(2,6,df.iloc[0]['Drug'])
ws1.update_cell(2,7,df.iloc[0]['Plan'])