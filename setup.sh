#!/bin/bash

#Setup Script for installing the python environment and all dependencies - pyhton needs to be installed
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install pandas tqdm pymupdf openpyxl xlrd

echo "Setup went well. Virtual Environment active and ready!"