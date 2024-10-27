import argparse, sys

from .utils import summarize_csv
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input-file',
        type=str
    )
    parser.add_argument(
        '--output-file',
        type = str
    )
    args=parser.parse_args()

    try:
        data = summarize_csv(args.input_file)
        if args.output_file is not None:
            with open(args.output_file, 'w', encoding='utf-8') as file:
                file.write(f'Доход: {data[0]}\nРасход: {data[1]}')
        else:
            print(f'Доход: {data[0]}')
            print(f'Расход: {data[1]}')
    except Exception as e:
        print(f'Ошибка: {e}')

if __name__ == '__main__':
    main()