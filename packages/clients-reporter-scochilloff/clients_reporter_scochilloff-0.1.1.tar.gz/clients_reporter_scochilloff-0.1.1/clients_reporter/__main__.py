from .utils import load_clients, write_report

import argparse


def main() -> None:
    parser = argparse.ArgumentParser("clients_reporter")
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--output-file", required=True)
    args = parser.parse_args()

    clients = load_clients(args.input_file)
    write_report(clients, args.output_file)


if __name__ == "__main__":
    main()
