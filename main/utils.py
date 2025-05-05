from main.paths import get_data_path



def write_csv(df, name:str = None):
    
    if name == None:
        raise ValueError("The 'name' parameter must be provided.")

    
    data_path = get_data_path()
    
    df.to_csv(data_path / name)
    
    return None