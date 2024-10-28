import pandas as pd

def stat_sales(old_file, new_file):
    df = pd.read_csv(old_file)
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
    df_grouped = df.groupby('category').sum(['sales', 'quantity'])
    df_grouped.to_csv(new_file)

__all__ = ['stat_sales']