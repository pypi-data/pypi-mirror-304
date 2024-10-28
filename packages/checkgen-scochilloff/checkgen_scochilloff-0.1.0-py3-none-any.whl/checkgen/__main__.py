from .utils import load_order, write_check

import argparse


def main() -> None:
    parser = argparse.ArgumentParser("checkgen")
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--output-file", required=True)
    args = parser.parse_args()

    order = load_order(args.input_file)
    write_check(order, args.output_file)


if __name__ == "__main__":
    main()