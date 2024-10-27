import argparse
from .utils import group

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-file",
        type=str
    )
    parser.add_argument(
        "--output-file",
        type=str
    )
    args = parser.parse_args()

    try:
        group(args.input_file, args.output_file)
        print("Группировка завершена")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
