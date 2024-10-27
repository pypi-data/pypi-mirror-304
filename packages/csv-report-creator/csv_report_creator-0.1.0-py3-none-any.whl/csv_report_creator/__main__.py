from .data_loading import load_data, write_data
from .data_processing import get_totals_by_categories

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(prog="csv_report_creator")
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--output-file", required=True)
    args = parser.parse_args()

    data = load_data(args.input_file)
    if data is None:
        print("Ошибка: Неверный тип файла или файл не существует")
        return
    totals_by_amounts = get_totals_by_categories(data)
    if totals_by_amounts is None:
        print("Ошибка: Неверный формат данных")
        return
    write_data(totals_by_amounts, args.output_file)



if __name__ == "__main__":
    main()
