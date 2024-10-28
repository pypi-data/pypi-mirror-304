import task_2

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input-file', type=str, required=True)
parser.add_argument('--output-file', type=str, required=True)

args = parser.parse_args()

task_2.to_txt(args.input_file, args.output_file)
