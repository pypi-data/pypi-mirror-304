import argparse
import json
from package_4 import generate_check

def main():
    parser = argparse.ArgumentParser(description="Генерация чека")
    parser.add_argument("--input-file", required=True, help="Путь к входному файлу .json")
    parser.add_argument("--output-file", required=True, help="Путь к выходному файлу .txt")
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as file:
        order_data = json.load(file)

    receipt = generate_check(order_data)

    with open(args.output_file, 'w', encoding='utf-8') as file:
        file.write(receipt)

if __name__ == "__main__":
    main()