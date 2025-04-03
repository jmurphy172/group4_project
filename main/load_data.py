from main.read_data import read_data 

import pandas as pd 

from pathlib import Path





class Load_data:
    
    
    def get_root_dir():
        return read_data.root() 
    
    def load_raw_data():
        
       root_dir = Load_data.get_root_dir()
       
       raw_data = pd.read_csv(root_dir / "raw_data/chess_games.csv")
       
       return raw_data
       
       
    
    
    
    
if __name__ == "__main__":
    
    root = Load_data.get_root_dir()
    
    raw_data = Load_data.load_raw_data()
    
    print(root)
