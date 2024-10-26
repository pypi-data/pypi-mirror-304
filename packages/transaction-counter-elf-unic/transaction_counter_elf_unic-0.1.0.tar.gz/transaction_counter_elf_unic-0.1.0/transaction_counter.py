import argparse
import pandas as pd


def count_category(in_file, out_file):
    table = pd.read_csv(in_file, index_col='transaction_id')
    table = table.groupby(['category']).sum()

    with open(out_file, 'w') as f:
        f.write(f"Доход: {table.loc['Доход']['amount']}\n")
        f.write(f"Расход: {table.loc['Расход']['amount']}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--input_file',
        action='store',
        required=True,
    )

    parser.add_argument(
        '--output_file',
        action='store',
        required=True,
    )

    args = parser.parse_args()

    count_category(args.input_file, args.output_file)


if __name__ == '__main__':
    main()
