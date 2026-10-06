# reads Excel file and returns object - DataFrame (table pandas), with structure like
#     DataFrame(Login),
#     DataFrame(User Registration),
#     DataFrame(Data Consent) ....

from typing import List
import pandas as pd
import os

def load_excel(file_path: str) -> List[pd.DataFrame]:
    """
        Opens .xlx file and creates list of DataFrames (pandas-tables).
        :param file_path: path to .xlx file
        :return: list of DataFrames
    """

    print("REAL FILE:", os.path.abspath(file_path))

    # open .xlx file
    excel_file = pd.ExcelFile(file_path)
    # gets sheet names
    print("Sheets:", excel_file.sheet_names)

    all_sheets = []

    for sheet_name in excel_file.sheet_names:
        # read sheet and create DataFrame
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        print(f"\nSheet: {sheet_name}")
        print(df.head())

        # add sheet to list
        all_sheets.append(df)

    return all_sheets
