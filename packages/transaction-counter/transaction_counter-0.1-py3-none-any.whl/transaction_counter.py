import pandas as pd
import argparse

def count_category(in_file, out_file):
    table = pd.read_csv(in_file, index_col='transaction_id')
    with open(out_file, 'w') as f:
        for name, row in table.groupby(by='category').agg('sum').iterrows():
            f.write(f'{name}: {row['amount']} руб.\n')


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--input',
        action='store',
        required=True,
    )

    parser.add_argument(
        '--output',
        action='store',
        required=True,
    )

    args = parser.parse_args()
    count_category(args.input, args.output)


if __name__ == '__main__':
    main()
