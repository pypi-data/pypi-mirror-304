import pandas as pd

def load_data(input_file):
    return pd.read_csv(input_file)

def generate_report(data):
    grouped = data.groupby("category").agg(
        sales=("sales", "sum"),
        quantity=("quantity", "sum")
    ).reset_index()
    return grouped

def save_report(report, output_file):
    report.to_csv(output_file, index=False)
