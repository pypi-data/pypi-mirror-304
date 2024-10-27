import pandas as pd

def group(csv_input_path, csv_output_path):
    df = pd.read_csv(csv_input_path)
    df_grouped = df.groupby('category')[['sales', 'quantity']].sum().reset_index()
    df_grouped.to_csv(csv_output_path, index=False)


