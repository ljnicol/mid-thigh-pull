

import pandas as pd
import numpy as np

from os import listdir, walk
from os.path import isfile, join

import argparse

parser = argparse.ArgumentParser(description='Process mid-thigh pull data files.')
parser.add_argument('data_directory', metavar='dir', type=str, nargs=1,
                   help='a directory containing your data files')

parser.add_argument('output_file', metavar='output', type=str, nargs=1,
                   help='output file')

args = parser.parse_args()
data_dir = vars(args)['data_directory'][0]
output_file = vars(args)['output_file'][0]

def process_data_file(filename):
    print ("Processing file: " + filename)

    df = pd.read_csv(filename, skiprows=lambda x: x < 17 or x == 18, sep='\t')
    df['force_magnitude'] = np.sqrt(np.square(df.Fx) + np.square(df.Fy) + np.square(df.Fz))
    df['force_gradient'] = np.gradient(df['force_magnitude'].rolling(center=False,window=4).sum())
    max_force= df.force_magnitude.max()
    max_force_at = df['force_magnitude'].idxmax()
    max_force_row = df.iloc[max_force_at]
    max_force_at_s = max_force_row['abs time (s)']

    max_gradient= df.force_gradient.max()
    max_gradient_at = df['force_gradient'].idxmax()
    max_gradient_row = df.iloc[max_gradient_at]
    max_gradient_at_s = max_gradient_row['abs time (s)']

    return [filename, max_force, max_force_at_s, max_gradient, max_gradient_at_s]

data_files = []
for path, subdirs, files in walk("data"):
    for name in files:
        data_files.append(join(path, name))

output = np.array(list(map(lambda filename: process_data_file(filename), data_files)))
out_df = pd.DataFrame(data=output, columns=['input_filename', 'max_force', 'max_force_at_s', 'max_gradient', 'max_gradient_at_s'])
out_df.to_csv(output_file)
