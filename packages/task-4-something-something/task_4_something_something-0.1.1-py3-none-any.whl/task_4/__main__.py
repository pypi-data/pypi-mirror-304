import task_4

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input-file', type=str, required=True)
parser.add_argument('--output-file', type=str, required=True)

args = parser.parse_args()

task_4.check(args.input_file, args.output_file)
