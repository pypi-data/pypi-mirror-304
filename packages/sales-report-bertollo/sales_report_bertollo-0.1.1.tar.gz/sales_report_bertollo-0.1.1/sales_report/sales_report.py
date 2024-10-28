import pandas as pd

def generate_report(input_file: str, output_file: str):
    data = pd.read_csv(input_file)

    report = data.groupby('category').agg(
        sales=('sales', 'sum'),
        quantity=('quantity', 'sum')
    ).reset_index()

    report.to_csv(output_file, index=False)
