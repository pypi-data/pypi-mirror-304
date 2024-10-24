import argparse
import os
import io

import pypdf as PDF
from more_itertools import consume


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', nargs='+')
    args = parser.parse_args()
    if not len(args.input_file) > 1:
        parser.error('at least two files must be specified')
    return args


def open_pdfs(names):
    for name in names:
        with open(name, 'rb') as f:
            buffer = io.BytesIO(f.read())
            yield PDF.PdfReader(buffer)


def do_merge(input_names, output_name):
    merged = PDF.PdfWriter()
    for in_pdf in open_pdfs(input_names):
        consume(map(merged.add_page, in_pdf.pages))
    with open(output_name, 'wb') as outf:
        merged.write(outf)


def main():
    input_names = get_args().input_file
    output_names = [os.path.splitext(os.path.basename(name))[0] for name in input_names]
    output_name = ' - '.join(output_names) + '.pdf'
    output_name = os.path.join(os.path.dirname(input_names[0]), output_name)
    do_merge(input_names, output_name)


if __name__ == '__main__':
    main()
    print("Press enter to continue")
    input()
