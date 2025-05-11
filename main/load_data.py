from main.paths import get_root_path

import pandas as pd 

from pathlib import Path

 
def load_raw_data():
    
   root_dir = get_root_path()
   
   raw_data = pd.read_csv(root_dir / "raw_data/filtered_chess_games.csv")
   
   return raw_data

  
    
if __name__ == "__main__":
    
    root = get_root_path()
    
    raw_data = load_raw_data()
    
    print(root)
    
    
    



