from main.load_data import load_raw_data

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
        main_opening, variation = opening_name.split(':', 1)
        if 'Gambit' in variation:
            return f"{main_opening}: {variation.strip()}"
        return main_opening.strip()
    return opening_name.strip()


def clean_openings_column(df):
    """
    Apply the clean_name function to the 'Opening' column of the dataframe.
    """
    df['Opening'] = df['Opening'].apply(clean_name)
    return df


def run_cleaning_pipeline():
    df = load_raw_data()
    df = drop_duplicates(df)
    df = clean_openings_column(df)  
    return df


if __name__ == "__main__":
    cleaned_df = run_cleaning_pipeline()
    print(f"✅ Final dataset shape: {cleaned_df.shape}")
    print(cleaned_df.head())
    
    
    cleaned_df.to_csv("cleaned_data.csv")

        


    
    
    

    
    
    
    
    

