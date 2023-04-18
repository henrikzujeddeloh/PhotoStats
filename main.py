import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from tabulate import tabulate
from PIL import Image, ExifTags
from pillow_heif import register_heif_opener

# set dimensiouns of visualizations
WIDTH = 10
HEIGHT = 5

TIMEZONE = 'Europe/Berlin'

# file extentions to ignore
ignore_ext = ('.md', '.MOV', '.mp4', '.CR2', '.RAF')

# returns specified EXIF tag value for image
def get_field (exif, field):
    for (k,v) in exif.items():
        if ExifTags.TAGS.get(k) == field:
            return v


def create_df(folder):

    # creates pandas DatFrame with relevant columns
    data_frame = pd.DataFrame(columns=('photo', 'capture_date', 'camera'))
    
    # loop through all directories and subdirectories
    i = 0
    for subdir, dirs, files in os.walk(folder):
        for filename in files:
            # ignores hidden files and files in ignore list
            if not filename.startswith('.') and not filename.endswith(ignore_ext):
                f = os.path.join(subdir, filename)
                if os.path.isfile(f):
                    img = Image.open(f)
                    img.verify()
                    # gets raw EXIF data for image
                    img_exif = img.getexif()

                    # if image has EXIF data it saves specified tag values in dataframe
                    if img_exif is None:
                        print("no EXIF data for " + f)
                    else:
                        capture_date = get_field(img_exif, 'DateTime')
                        camera = get_field(img_exif, 'Model')
                        data_frame.loc[i] = [filename, capture_date, camera]
                        i +=1
    return data_frame

# instantiates argument parser
parser = argparse.ArgumentParser()
parser.add_argument("folder_path", help="path to photos directory which should be scanned")
args = parser.parse_args()

# function to open HEIF files
register_heif_opener()

# creates pandas DataFrame
df = create_df(args.folder_path)





print(df)
print(df.info(memory_usage='deep'))
