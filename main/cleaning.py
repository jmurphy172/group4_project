from main.load_data import load_raw_data

from main.utils import write_csv

import pandas as pd



# =============================================================================
#  Added in a little bit of cleaning when I found aliases in analysis phase
# =============================================================================

PETROV_ALIASES = {
    "Russian Game": "Petrov",
    "Petrov's Defense": "Petrov",
}


def standardize_petrov_openings(df):
    """
    Standardizes Petrov-related opening names using predefined aliases.
    """
    df['opening'] = df['opening'].replace(PETROV_ALIASES)
    return df




def drop_duplicates(df):
    """
    Drop duplicate games keeping only the first appearance per White and per Black player.
    """
    df = df.drop_duplicates(subset=["White"])
    df = df.drop_duplicates(subset=["Black"])
    return df.reset_index(drop=True)




def clean_name(opening_name):
    
    
    """
    
    Strips whitespace, splits on the first “:”.
    
    If the variation part contains “Gambit”, 
    
    it returns “Main : Variation”;
    
    otherwise it drops the variation and returns only the main opening name.
    
    
    
    Some openings that might be considered distinctive are perhaps not properly segregated, e.g.


		Russian Game: Paulsen Attack
		Russian Game: Nimzowitsch Attack
		Petrov: Modern Attack


    A tag that ends in “Attack” can be anything from a full-blown repertoire choice (King’s Indian Attack)
    to a minor sideline like the Nimzowitsch Attack versus the Petrov.
    
    
    We did not have scope to measure each one’s frequency, we mapped them back to the parent opening.
    
    
    Gambits stay separate because—even when rare—they reshape the game outright.

    
    
    """
    
    
    
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



def make_all_col_names_lowercase(df):
    
    df.columns = df.columns.str.lower()
    
    return df




def calculate_rating_diff_for_nans(df):
    
    condition_white_nan = df["whiteratingdiff"].isna()
    condition_black_nan = df["blackratingdiff"].isna()

    df.loc[condition_white_nan, "whiteratingdiff"] = df["whiteelo"] - df["blackelo"]
    df.loc[condition_black_nan, "blackratingdiff"] = df["blackelo"] - df["whiteelo"]

    return df


def remove_rating_diffs_greater_than_fifty_points(df):
    """
    Removes rows where either white or black rating difference exceeds 50 points.
    """
    condition = (df["whiteratingdiff"].abs() <= 50) & (df["blackratingdiff"].abs() <= 50)
    return df[condition].reset_index(drop=True)


def beginners_only(df):
    
    """
    This function removes players rated below 1000 and players rated above 2000
    
    or keeps players where the following condition is true.
    
    1000 < elo < 2000 (inclusive)  
    
    """
    
    df = df[df["whiteelo"] > 999]
    
    df = df[df["whiteelo"] < 2001]
    
    df = df[df["blackelo"] > 999]
    
    df = df[df["blackelo"] < 2001]
    
    
    return df







def run_cleaning_pipeline():
    
    df = load_raw_data()
    df = drop_duplicates(df)
    df = clean_openings_column(df) 
    df = make_all_col_names_lowercase(df)
    df = beginners_only(df)
    
    
    
    
    # decided to drop these after
    # we couldn't find a use for them in analysis
    df = df.drop(columns= ["moves", "timecontrol"])
    
    
    
    
    df = standardize_petrov_openings(df)
    
    
    df = calculate_rating_diff_for_nans(df)
    
    df = remove_rating_diffs_greater_than_fifty_points(df)
    
    
    
    
    
    return df


if __name__ == "__main__":
    
    
    
    
    cleaned_df = run_cleaning_pipeline()
    
    
    
    print(f"Final dataset shape: {cleaned_df.shape}")
    print(cleaned_df.head())
    

    write_csv(cleaned_df, "cleaned_df.csv")

