import argparse
from . import groups_from_csv

def main(args):
    groups_from_csv(args.input_file, args.output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', action='store')
    parser.add_argument('--output-file', action='store')

    args = parser.parse_args()
    main(args)