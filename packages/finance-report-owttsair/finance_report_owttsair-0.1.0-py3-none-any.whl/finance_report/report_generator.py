import pandas as pd

def load_data(input_file):
    return pd.read_csv(input_file)

def calculate_totals(data):
    grouped = data.groupby("category")["amount"].sum()
    return grouped.to_dict()

def save_report(totals, output_file):
    with open(output_file, "w") as f:
        for category, total in totals.items():
            f.write(f"{category.capitalize()}: {total} руб.\n")
