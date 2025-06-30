import pandas as pd
from main.paths import get_data_path

import numpy as np
import pandas as pd





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
    
    
