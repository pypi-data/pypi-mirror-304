import argparse
from receipt_generator.generator import load_order_data, generate_receipt, save_receipt


def main():
    parser = argparse.ArgumentParser(description="Генератор чеков для заказов.")
    parser.add_argument("--input-file", required=True, help="Путь к входному JSON-файлу с данными о заказе")
    parser.add_argument("--output-file", required=True, help="Путь к выходному текстовому файлу для чека")

    args = parser.parse_args()

    order_data = load_order_data(args.input_file)
    receipt = generate_receipt(order_data)
    save_receipt(receipt, args.output_file)

    print(f"Чек успешно сохранен в файл {args.output_file}")
