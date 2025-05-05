from pathlib import Path 

 
    
def get_root_path():
    
    return Path(__file__).resolve().parent.parent  


def get_data_path():
    
    root = get_root_path()
    
    data_path = root / "main" / "data"
    
    return data_path
  
    

if __name__ == "__main__":
    
    

    root = get_root_path() 
    print(root)



    data_path = get_data_path()
    
    print (data_path)