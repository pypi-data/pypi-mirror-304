import pandas as pd


def load_transactions(input_file):
    df = pd.read_csv(input_file)
    return df


def generate_report(transactions):
    report = transactions.groupby('category')['amount'].sum().reset_index()

    report_lines = [
        (
            f"{row["category"].capitalize()}: "
            f"{row["amount"]:.2f} руб."
        ) for _, row in report.iterrows()
    ]

    return '\n'.join(report_lines)
