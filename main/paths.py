from pathlib import Path 

 
    
def get_root_path():
    
    return Path(__file__).resolve().parent.parent  
  
    

if __name__ == "__main__":
    
    

    root = get_root_path() 
    print(root)
