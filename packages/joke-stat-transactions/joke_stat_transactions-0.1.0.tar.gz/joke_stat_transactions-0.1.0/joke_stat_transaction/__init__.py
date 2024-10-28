import pandas as pd
def groups_from_csv(csv_file, txt_file):
    df = pd.read_csv(csv_file)
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
    df = df.reset_index(drop=True)
    df_groups = df.groupby(['category', 'type']).sum('money')
    df_res = df_groups.to_string()
    with open(txt_file, 'w') as res_file:
        res_file.writelines(df_res)

__all__ = ['groups_from_csv']