# python download_images_from_csv.py '../data/imgur.csv' '../data/fake'

import pandas as pd
import requests
import urllib
import os
import sys
from datetime import datetime

CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else 'data/imgur.csv'
OUTPUT_PATH = sys.argv[2] if len(sys.argv) > 2 else 'data/fake'

def images_from_file_path(file_path):
    file_names = os.listdir(file_path)
    return file_names

def Main():
    print("START TIME ", str(datetime.now()))
    df = pd.read_csv(CSV_PATH, index_col=0)
    df = df.reset_index()
    df['file_name'] = df['index']

    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    output_images = images_from_file_path(OUTPUT_PATH)

    downloaded_count = 0
    for idx, vals in df.iterrows():
        url = vals['url']
        filename = str(vals['file_name']) + '.jpg'
        if filename not in output_images:
            path = OUTPUT_PATH + '/' + filename
            print filename
            urllib.urlretrieve(url, path)
            downloaded_count += 1
            print'Downloaded: ', downloaded_count

    print("Finished Downloading ", str(datetime.now()))

if __name__ == '__main__':
    Main()
