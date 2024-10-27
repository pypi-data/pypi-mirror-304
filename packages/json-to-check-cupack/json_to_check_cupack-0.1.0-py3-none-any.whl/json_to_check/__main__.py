import argparse

from dateutil.parser import parser

from .utils import json_to_check

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input-file',
        type=str
    )
    parser.add_argument(
        '--output-file',
        type=str
    )
    args = parser.parse_args()

    try:
        json_to_check(args.input_file, args.output_file)
        print('Формирование чека завершено.')
    except Exception as e:
        print(f'Ошибка: {e}')

if __name__ == '__main__':
    main()