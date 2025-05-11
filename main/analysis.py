import pandas as pd
from scipy.stats import binomtest, chi2_contingency
import matplotlib.pyplot as plt



from main.utils import write_csv, read_csv

from main.load_data import load_raw_data


import pprint as pretty


from main.cleaning import make_all_col_names_lowercase



_show_graphs = False

_analysis = False

_debug = True


#%% Definitions


def get_top_n_openings(unique_openings_with_counts, n):
    
    unique_openings_with_counts = make_all_col_names_lowercase(unique_openings_with_counts)
    
    unique_openings_with_counts = unique_openings_with_counts.sort_values("count", ascending=False)
    
    top_openings = unique_openings_with_counts.head(n)
    
    return top_openings

#%%
def get_unique_openings_with_counts(df):
    
    
    df = make_all_col_names_lowercase(df)
    
    unique_openings_with_counts =(
        
        df['opening'].value_counts()
        
                        .reset_index()
                        
                            .sort_values("count", ascending=False)
                                                               
                            )
    
    
    
    return unique_openings_with_counts



#%% explore raw data

RAW_DATA = load_raw_data()


unique_openings_from_RAW_DATA = get_unique_openings_with_counts(RAW_DATA)


write_csv(unique_openings_from_RAW_DATA, "unique_openings_from_RAW_DATA.csv")





#%% Load cleaned data
_cleaned_df = read_csv("cleaned_df.csv")

#%% find uncommon openings


# Step 1: Get all unique openings with their counts
unique_openings_with_counts_from__cleaned_df = get_unique_openings_with_counts(_cleaned_df)
    
  
#%% let us define cleaned data that is going through various transformations as the as the following:
    
    
dft = _cleaned_df.copy()

#%%


# Step 2: Merge the DataFrames on the 'opening' column
dft = dft.merge(unique_openings_with_counts_from__cleaned_df, on='opening', how='left').sort_values("count", ascending=False)

#%%


# Step 3: rename column

dft.rename(columns = {'count':'opening_count'})



#%%



# Calculate the total count
total_count = unique_openings_with_counts_from__cleaned_df['count'].sum()

# Create a new column 'percentage'
unique_openings_with_counts_from__cleaned_df['percentage'] = (unique_openings_with_counts_from__cleaned_df['count'] / total_count) * 100

# Round the percentage to 2 decimal places
unique_openings_with_counts_from__cleaned_df['percentage'] = unique_openings_with_counts_from__cleaned_df['percentage'].round(2)

unique_openings_with_counts_from__cleaned_df = unique_openings_with_counts_from__cleaned_df.sort_values(by='percentage', ascending=False)



#%% Top openings

top_70_openings = get_top_n_openings(unique_openings_with_counts_from__cleaned_df, 70)


top_70_openings.to_csv("top_70_openings.csv")



#%% sort for graphing purposes

unique_openings_with_counts_from__cleaned_df = unique_openings_with_counts_from__cleaned_df.sort_values(by='percentage', ascending=True)


write_csv(unique_openings_with_counts_from__cleaned_df, "unique_openings_with_counts_from__cleaned_df.csv")

#%% plot all openings

if _show_graphs:
    
    
    # Create the horizontal bar plot
    plt.figure(figsize=(10, 8))
    plt.barh(unique_openings_with_counts_from__cleaned_df['opening'], unique_openings_with_counts_from__cleaned_df['percentage'], color='skyblue')
    
    plt.xlabel('Percentage of Games (%)')
    plt.title('Chess openings by Percentage of Games')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    
    plt.tight_layout()
    
    plt.show()
    
    
    

#%%


def plot_top_n_openings_improved(n):
    
    from matplotlib.ticker import MaxNLocator, AutoMinorLocator
    
    top_n_openings = get_top_n_openings(unique_openings_with_counts_from__cleaned_df, n)
    
    # Sort in descending order for better visualization
    top_n_openings = top_n_openings.sort_values(by='percentage', ascending=True)
    
    
    top_n_openings_coverage_percentage = top_n_openings.percentage.sum().round(2)
    
    
    
    # Create the horizontal bar plot
    fig, ax = plt.subplots(figsize=(20, 10))  # figsize = (horizontal,vertical)
    
    
    bars = ax.barh(top_n_openings['opening'], top_n_openings['percentage'], color='skyblue', align='center')
    
    # Adjust x-axis ticks for better readability
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # Cleaner x-axis numbers
    
    # Add minor ticks to x-axis only
    ax.xaxis.set_minor_locator(AutoMinorLocator(4))  # This adds minor ticks to x-axis
    
    # Add labels and title
    ax.set_xlabel('Percentage of Games (%)', fontsize=12)
    ax.set_title(f'Top {n} Chess openings by Percentage of Games', fontsize=14, pad=15)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Adjust margins and spacing
    plt.subplots_adjust(left=0.25, right=0.95)  # Reduced left margin
    # Improve spacing and layout
    ax.set_yticks(range(len(top_n_openings)))
    ax.set_yticklabels(top_n_openings['opening'], fontsize=10)
    
    # Enable x-axis minor ticks grid
    ax.grid(axis='x', linestyle=':', alpha=0.5, which='minor')
    
    
    # Add a text box with the coverage percentage
    textstr = f'These {n} openings represent {top_n_openings_coverage_percentage}% of all games'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    
    ax.text(0.75, 0.75, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='bottom', horizontalalignment='right', bbox=props)
    
    
    plt.tight_layout()
    
    plt.show()
    
    
    
    
# Call the improved function

if _show_graphs:
    
    plot_top_n_openings_improved(70)
    
    plot_top_n_openings_improved(30)




#%% Top openings

top_30_openings = get_top_n_openings(unique_openings_with_counts_from__cleaned_df, n = 30)


write_csv(top_30_openings, "top_30_openings.csv")


top_30_openings_coverage_percentage = top_30_openings.percentage.sum().round(2)


if _analysis:
    print(f"\n\nThe top thirty openings account for {top_30_openings_coverage_percentage}% of the total games\n\n")






#%% All games including russian or petrov


opening_name_investigation_from_raw = RAW_DATA[RAW_DATA["opening"].str.contains("russian", case=False, na=False) |
                                      RAW_DATA["opening"].str.contains("petrov", case=False, na=False)]




opening_name_investigation_from_raw = get_unique_openings_with_counts(opening_name_investigation_from_raw)

write_csv(opening_name_investigation_from_raw, "opening_name_investigation_from_raw.csv" )


############


opening_name_investigation_from_clean = _cleaned_df[_cleaned_df["opening"].str.contains("russian", case=False, na=False) |
                                      _cleaned_df["opening"].str.contains("petrov", case=False, na=False)]



opening_name_investigation_from_clean = get_unique_openings_with_counts(opening_name_investigation_from_clean)

write_csv(opening_name_investigation_from_clean, "opening_name_investigation_from_clean.csv" )



#%% classify top 30


if _debug:

    
    # Assuming top_30_openings is a DataFrame with an "opening" column
    responsibilities = [(opening, '') for opening in top_30_openings["opening"]]
    
    pretty.pprint(responsibilities)




    responsibilities = [
     
     ('Sicilian Defense', ''),
     
     ("Queen's Pawn Game", ''),
     
     ("King's Pawn Game", ''),
     
     ('French Defense', ''),
     
     ('Philidor Defense', ''),
     
     ('Italian Game', ''),
     
     ('Scandinavian Defense', ''),
     
     ('Ruy Lopez', ''),
     
     ('English opening', ''),
     
     ("Bishop's opening", ''),
     
     ('Caro-Kann Defense', ''),
     
     ('Scotch Game', ''),
     
     ('Four Knights Game', ''),
     
     ("Van't Kruijs opening", ''),
     
     ("Queen's Gambit Declined", ''),
     
     ("Queen's Gambit Accepted", ''),
     
     ('Modern Defense', ''),
     
     ('Nimzowitsch Defense', ''),
     
     ('Indian Game', ''),
     
     ("Queen's Gambit Refused", ''),
     
     ('Horwitz Defense', ''),
     
     ('Pirc Defense', ''),
     
     ("King's Knight opening", ''),
     
     ('Center Game', ''),
     
     ('Vienna Game', ''),
     
     ('Owen Defense', ''),
     
     ('Hungarian opening', ''),
     
     ('Slav Defense', ''),
     
     ('Alekhine Defense', ''),
     
     ('Three Knights opening', '')
     
     
     
     ]
    
    print("\n\n\n\n")
    
    
    # Apply the rule: if "Defense" is in the opening name, assign "black"; otherwise, assign nothing
    responsibilities = [
        
        (opening, 'black' if 'Defense' in opening else '') for opening, responsibilty in responsibilities
        
        ]
    
    # Print the updated list
    for ITEM in responsibilities:
        print(f"{ITEM},")
        print()  # Print an empty line for spacing 
        
    
        
responsibilities =[
    
        ('Sicilian Defense', 'black'),
        
        ("Queen's Pawn Game", 'white'),
        
        ("King's Pawn Game", 'white'),
        
        ('French Defense', 'black'),
        
        ('Philidor Defense', 'black'),
        
        ('Italian Game', 'white'),
        
        ('Scandinavian Defense', 'black'),
        
        ('Ruy Lopez', 'white'),
        
        ('English opening', 'white'),
        
        ("Bishop's opening", 'white'),
        
        ('Caro-Kann Defense', 'black'),
        
        ('Scotch Game', 'white'),
        
        ('Four Knights Game', 'white'),
        
        ("Van't Kruijs opening", 'white'),
        
        ("Queen's Gambit Declined", 'black'),
        
        ("Queen's Gambit Accepted", 'black'),
        
        ('Modern Defense', 'black'),
        
        ('Nimzowitsch Defense', 'black'),
        
        ('Indian Game', 'black'),
        
        ("Queen's Gambit Refused", 'black'),
        
        ('Horwitz Defense', 'black'),
        
        ('Pirc Defense', 'black'),
        
        ("King's Knight opening", 'white'),
        
        ('Center Game', 'white'),
        
        ('Vienna Game', 'white'),
        
        ('Owen Defense', 'black'),
        
        ('Hungarian opening', 'white'), # ??? check
        
        ('Slav Defense', 'black'),
        
        ('Alekhine Defense', 'black'),
        
        ('Three Knights opening', 'white'),

]


responsibilities = pd.DataFrame(responsibilities)


responsibilities = responsibilities.rename(columns= { 
    
                                                     0: "opening",
                                                     
                                                     1: "responsibility" 
                                                     
                                                     }
                                           )


