import pandas as pd
from main.paths import get_data_path

import numpy as np
import pandas as pd
import inspect

import xlwings as xw


import threading

import time

import subprocess
import tempfile
import os




def write_csv(df, name:str = None):
    
    if name == None:
        raise ValueError("The 'name' parameter must be provided.")

    
    data_path = get_data_path()
    
    df.to_csv(data_path / name, index=False)
    
    return None



def read_csv(name:str = None):
    
    if name == None:
        raise ValueError("The 'name' parameter must be provided.")

    
    data_path = get_data_path()
    
    csv = pd.read_csv(data_path / name)
    
    return csv
    
    
#%% df utils

def df_difference(big_boi:pd.DataFrame, smol_boi:pd.DataFrame) -> pd.DataFrame:
    
    """
    Return rows from `big_boi` that do not appear in `smol_boi`.
    
    This function performs a "row-wise" difference (sometimes called an anti-join):
    it identifies all rows that are present in `big_boi` but not in `smol_boi`.
    Despite the playful names, there's no requirement that `big_boi` actually be 
    larger than `smol_boi`; these labels simply reflect a common scenario where 
    you remove rows from a large dataset using a smaller reference set. 
    
    Duplicates in `big_boi` will be preserved unless they also appear in `smol_boi`.
    
    Parameters
    ----------
    big_boi : pd.DataFrame
        The "larger" DataFrame from which rows are subtracted. (Its size is immaterial;
        you can think of it as the one you primarily want to filter.)
    smol_boi : pd.DataFrame
        The "smaller" (or reference) DataFrame containing rows to remove from `big_boi`.
        It doesn't need to be smaller in reality—it's just labeled that way here for
        convenience or fun.
    
    Returns
    -------
    pd.DataFrame
        All rows from `big_boi` that are not present in `smol_boi`.
    
    Notes
    -----
    - This function merges on all columns with the same names in both DataFrames. If you only
      want to compare a subset of columns, adjust the `merge` call accordingly.
    - Rows that match exactly (same values in all columns used for the merge) in both
      DataFrames are removed from the result. 
    - The difference preserves duplicates from `big_boi` unless those duplicates are 
      also found in `smol_boi`.
    - The choice of names (`big_boi` and `smol_boi`) is arbitrary and a bit tongue-in-cheek:
      the function works no matter the actual sizes of the DataFrames.
    """

    df_diff =(
        
        pd.merge(big_boi, smol_boi,

                 how = "outer",
                 indicator = True)
                .query(

                    '_merge == "left_only"'

                        ).drop(

                            columns = ["_merge"]

                                )
                        
                    )

    return df_diff






def dcl(df):
    """Print the dataframe column names in the desired format."""
    # Retrieve the name of the variable passed into the function
    frame = inspect.currentframe().f_back
    df_name = [name for name, value in frame.f_locals.items() if value is df][0]
    
    formatted_output = f"\n{df_name}[[\n\n" + ",\n\n".join(f"'{column}'" for column in df.columns) + "\n]]"
    print(formatted_output)
    
    
    
def is_view(df_1, df_2):
    
    print (np.shares_memory(df_1, df_2))
    
    
    

def move_column(df: pd.DataFrame, column_name: str, new_position: int) -> pd.DataFrame:
    """
    Move a column to a new position in a DataFrame.

    Parameters:
    df (pd.DataFrame): The original DataFrame.
    column_name (str): The name of the column to move.
    new_position (int): The index position to insert the column at (0-based).

    Returns:
    pd.DataFrame: A new DataFrame with the column reordered.
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    
    cols = [col for col in df.columns if col != column_name]
    cols.insert(new_position, column_name)
    return df[cols]




import os




def view_df(df: pd.DataFrame | pd.Series) -> None:
    
    soffice = r"C:\Program Files\LibreOffice\program\soffice.exe"
    tmp_path = ""

    def delayed_delete(path, delay=5, retries=5, interval=2):
        def _delete():
            time.sleep(delay)
            for attempt in range(retries):
                try:
                    if os.path.exists(path):
                        os.unlink(path)
                        return  # success!
                except PermissionError:
                    time.sleep(interval)
                except Exception as e:
                    print(f"Cleanup failed on attempt {attempt + 1}: {e}")
                    break
        threading.Thread(target=_delete, daemon=True).start()


    try:
        
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            (df.to_frame() if isinstance(df, pd.Series) else df).to_csv(tmp.name, index=False)
            tmp_path = tmp.name
            
        subprocess.Popen([soffice, "--calc", tmp_path])  # non-blocking
        
        
    except Exception:
        wb = xw.Book()
        wb.sheets[0].range("A1").value = df
    finally:
        if tmp_path:
            delayed_delete(tmp_path)

    

