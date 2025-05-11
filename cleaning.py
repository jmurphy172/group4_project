from main.load_data import load_raw_data

from main.utils import write_csv

import pandas as pd



def drop_duplicates(df):
    """
    Drop duplicate games keeping only the first appearance per White and per Black player.
    """
    df = df.drop_duplicates(subset=["White"])
    df = df.drop_duplicates(subset=["Black"])
    return df.reset_index(drop=True)




def clean_name(opening_name):
    
    if ':' in opening_name:
        
        main_opening, variation = opening_name.split(':', maxsplit=1)
        
        
        
        
        if 'Gambit' in variation:
            
            return f"{main_opening}: {variation.strip()}"
        
        return main_opening.strip()
    
    
    return opening_name.strip()

    
    
    
def remove_numbered_games(opening_name):
    
    if "#" in opening_name:
        
        name, number = opening_name.split("#", maxsplit=1 )
        
        return name.strip()
    
    return opening_name
    



def clean_openings_column(df):
    """
    Apply the clean_name function to the 'Opening' column of the dataframe.
    """
    df['Opening'] = df['Opening'].apply(clean_name)
    
    df['Opening'] = df['Opening'].apply(remove_numbered_games)
    
    return df


def run_cleaning_pipeline():
    df = load_raw_data()
    df = drop_duplicates(df)
    df = clean_openings_column(df)  
    return df


if __name__ == "__main__":
    
    raw_data = load_raw_data()
    
    write_csv(raw_data, "raw_data.csv")
    
    
    
    cleaned_df = run_cleaning_pipeline()
    print(f"Final dataset shape: {cleaned_df.shape}")
    print(cleaned_df.head())
    

    write_csv(cleaned_df, "cleaned_data.csv")

