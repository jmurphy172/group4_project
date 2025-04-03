from pathlib import Path 

class read_data:
   
    
    def _base_path():
        
        return "C:/Users/James/OneDrive/Desktop/GitHub/group4_project"
    
    
    def root():
        
        return Path(__file__).resolve().parent.parent  # Works in scripts
      
    

if __name__ == "__main__":
    
    data = read_data._base_path() 
    print(data)

    root = read_data.root() 
    print(root)
