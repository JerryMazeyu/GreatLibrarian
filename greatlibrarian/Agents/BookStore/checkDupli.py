import csv
import pandas as pd


def remove_duplicates(csv_file):
    """check the duplicate in csv and remain the only one"""

    df = pd.read_csv(csv_file)
    dupli_rows = df[df.duplicated(keep=False)]

    if not dupli_rows.empty:
        print(f"Duplicate rows found:{dupli_rows}")
        unique_dupli = df.drop_duplicates(keep='first')
        unique_dupli.to_csv(csv_file, index=False)

        # df.drop_duplicates(keep=False,inplace=True)
        # df.to_csv(csv_file,index=False)
        print('Duplicates removed successfully!Remain one')
    else:
        print('No duplicates found.')


remove_duplicates(
    'Agents/BookStore/RawData/Area Studies/African American Studies.csv')
