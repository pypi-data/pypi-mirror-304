
from .utils import customer_stat
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-file",
        type=str
    )
    parser.add_argument(
        '--output-file',
        type=str
    )
    args=parser.parse_args()
    try:
        customer_stat(args.input_file, args.output_file)
        print("Текстовый файл с отчетом по таблице создан")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    main()