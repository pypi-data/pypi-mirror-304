import argparse
import pandas as pd

def generate_report(input_file: str, output_file: str):
    data = pd.read_csv(input_file)
    report = data.groupby('category')
    res = pd.DataFrame(columns=['category','sales','quantity'])
    for key, values in report:
        row = pd.DataFrame({'category': [str(key)],
                            'sales': [values['sales'].sum()],
                            'quantity': [values['quantity'].sum()]})
        res = pd.concat([res, row], ignore_index=True)
    res.to_csv(output_file, index=False)
    print(f"Отчёт сохранён в файл {output_file}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input-file',
        type=str,
        required=True)
    parser.add_argument(
        '--output-file',
        type=str, 
        required=True)

    args = parser.parse_args()
    generate_report(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
