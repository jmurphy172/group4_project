from main.load_data import Load_data

import pandas as pd

class Cleaning:

    def load_raw_data():
        raw_data = Load_data.load_raw_data()
        return raw_data

    def drop_duplicates(df):
        # Drop duplicates based on all columns
        deduplicated = df.drop_duplicates()

        # Drop duplicates based on the "White" column
        deduplicated = deduplicated.drop_duplicates(subset=["White"])
        
        """
        This reduced the number of rows from 121332 to 4247
        
        a difference of 117085
        
        """
        
        # Drop duplicates based on the "Black" column
        deduplicated = deduplicated.drop_duplicates(subset=["Black"])
        
        
        deduplicated = deduplicated.reset_index()
        
        
        """
        
        This reduced the number of rows from 4247 to 1573
        
        a difference of 2674
        
        
        """

        return deduplicated
    
    def remove_unnecessary_columns(df):
        
        # Remove unnecessary columns
        less_columns = deduplicated[
            [
                "Event",
                "White",
                "Black",
                "Result",
                "WhiteElo",
                "BlackElo",
                "WhiteRatingDiff",
                "BlackRatingDiff",
                "Opening",
                "TimeControl",
                "Moves"
            ]
        ]
        
        return less_columns
    
    
    def filter_to_classical_games(df):
        
        classical_games = df.query("Event == 'Rated Classical game'")
        
        return classical_games
    
    
    def remove_draws(df):
        
        no_draws = df.query("Result != '1/2-1/2'")
        
        return no_draws
    
    import pandas as pd
    
    def remove_high_difference_in_elo(df, threshold=300):
        """
        Remove rows where the difference in Elo ratings between players
        is greater than the specified threshold.
        
        Parameters:
        df (pd.DataFrame): Input DataFrame with WhiteElo and BlackElo columns
        threshold (int): Maximum allowed difference in Elo ratings
        
        Returns:
        pd.DataFrame: Filtered DataFrame
        """
        # Create a copy to avoid SettingWithCopyWarning
        filtered_df = df.copy()
        
        # Convert Elo columns to numeric values
        filtered_df["WhiteElo"] = pd.to_numeric(filtered_df["WhiteElo"], errors='coerce')
        filtered_df["BlackElo"] = pd.to_numeric(filtered_df["BlackElo"], errors='coerce')
        
        # Drop rows with non-numeric Elo values
        filtered_df = filtered_df.dropna(subset=["WhiteElo", "BlackElo"])
        
        # Calculate the absolute difference in Elo ratings
        filtered_df['difference_in_elo'] = abs(filtered_df["WhiteElo"] - filtered_df["BlackElo"])
        
        # Filter out rows where the difference is greater than the threshold
        filtered_df = filtered_df[filtered_df['difference_in_elo'] <= threshold]
        
        # Drop the temporary column
        filtered_df = filtered_df.drop(columns=['difference_in_elo'])
        
        return filtered_df
    
    
    def remove_new_comers(df):
        
        
       no_new_comers = df.query("-50 <= WhiteRatingDiff <= 50")
       
       no_new_comers = no_new_comers.query("-50 <= BlackRatingDiff <= 50")
       
       return no_new_comers
        


    
    
    
if __name__ == "__main__":
    
    raw_data = Cleaning.load_raw_data()
    
    deduplicated = Cleaning.drop_duplicates(raw_data)

    less_columns = Cleaning.remove_unnecessary_columns(deduplicated)
    
    classical_games = Cleaning.filter_to_classical_games(less_columns)
    
    no_draws = Cleaning.remove_draws(classical_games)
    
    similar_elos = Cleaning.remove_high_difference_in_elo(no_draws, 200)
    
    no_new_comers = Cleaning.remove_new_comers(similar_elos)
    
    
    
    
    

