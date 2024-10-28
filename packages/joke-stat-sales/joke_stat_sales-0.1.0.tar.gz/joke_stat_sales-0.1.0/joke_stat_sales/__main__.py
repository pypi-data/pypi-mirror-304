import argparse

from joke_stat_sales import stat_sales

def main(args):
    stat_sales(args.input_file, args.output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', action='store')
    parser.add_argument('--output-file', action='store')

    args = parser.parse_args()
    main(args)