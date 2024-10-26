import pandas as pd
import argparse


def age_group(age: int):
    if 18 <= age <= 25:
        return "18-25"
    elif 26 <= age <= 35:
        return "26-35"
    elif 36 <= age <= 45:
        return "36-45"
    elif 46 <= age <= 60:
        return "46-60"
    else:
        return "60+"


def analyze_customers(input_file: str, output_file: str):
    table = pd.read_csv(input_file, index_col='customer_id')
    total_customers = len(table)
    table['age_group'] = table['age'].apply(age_group)
    with open(output_file, 'w') as f:
        f.write(f'Общее количество клиентов: {total_customers}\n\n')
        f.write('Количество клиентов по возрастным группам:/n')
        for e in sorted(table['age_group'].unique()):
            f.write(f'{e}: {table['age_group'].value_counts()[e]}\n')
        f.write('\nРаспределение клиентов по городам:\n')
        for e in table['city'].unique():
            f.write(f'{e}: {table['city'].value_counts()[e]}\n')






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


    analyze_customers(args.input_file, args.output_file)


if __name__ == '__main__':
    main()
