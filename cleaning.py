import main.load_data as ld

import pandas as pd

import pandas as pd
import main.load_data as ld


def load_raw_data():
    return ld.load_raw_data()


def drop_duplicates(df):
    """
    Drop duplicate games keeping only the first appearance per White and per Black player.
    """
    df = df.drop_duplicates(subset=["White"])
    df = df.drop_duplicates(subset=["Black"])
    return df.reset_index(drop=True)


def remove_unnecessary_columns(df):
    return df[
        [
            "Event", "White", "Black", "Result",
            "WhiteElo", "BlackElo",
            "WhiteRatingDiff", "BlackRatingDiff",
            "Opening", "TimeControl", "Moves"
        ]
    ]


def filter_to_classical_games(df):
    return df.query("Event == 'Rated Classical game'")


def remove_draws(df):
    return df.query("Result != '1/2-1/2'")


def remove_high_difference_in_elo(df, threshold=300):
    """
    Remove rows where the Elo difference exceeds the threshold.
    """
    df = df.copy()
    df["WhiteElo"] = pd.to_numeric(df["WhiteElo"], errors="coerce")
    df["BlackElo"] = pd.to_numeric(df["BlackElo"], errors="coerce")
    df = df.dropna(subset=["WhiteElo", "BlackElo"])

    df["elo_diff"] = abs(df["WhiteElo"] - df["BlackElo"])
    df = df[df["elo_diff"] <= threshold]

    return df.drop(columns=["elo_diff"])


def remove_new_comers(df):
    """
    Keep only players whose rating changed by ±50 or less.
    """
    return df.query(
        "(-50 <= WhiteRatingDiff <= 50) and (-50 <= BlackRatingDiff <= 50)"
    )



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


def run_cleaning_pipeline(elo_threshold=200):
    df = load_raw_data()
    df = drop_duplicates(df)
    df = remove_unnecessary_columns(df)
    df = filter_to_classical_games(df)
    df = remove_draws(df)
    df = remove_high_difference_in_elo(df, threshold=elo_threshold)
    df = remove_new_comers(df)
    df = clean_openings_column(df)  
    return df


if __name__ == "__main__":
    cleaned_df = run_cleaning_pipeline()
    print(f"✅ Final dataset shape: {cleaned_df.shape}")
    print(cleaned_df.head())
    
    
    cleaned_df.to_csv("cleaned_data.csv")

        


    
    
    

    
    
    
    
    

