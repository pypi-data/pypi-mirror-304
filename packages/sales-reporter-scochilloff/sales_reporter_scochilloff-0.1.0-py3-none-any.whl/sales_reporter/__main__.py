import argparse

from .data_processing import process_data
from .data_in_out import load_data, output_data


def main() -> None:
    parser = argparse.ArgumentParser("sales_reporter")
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--output-file", required=True)
    args = parser.parse_args()

    try:
        data = load_data(args.input_file)
    except FileNotFoundError:
        print("Ошибка: Файл не найден")
        return
    except ValueError:
        print("Ошибка: Неправильный тип файла или формат данных")
        return
    processed_data = process_data(data)
    try:
        output_data(processed_data, args.output_file)
    except ValueError:
        print("Ошибка: Неправильный тип выходного файла")


if __name__ == "__main__":
    main()
