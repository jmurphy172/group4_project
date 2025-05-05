import pandas as pd
from scipy.stats import binomtest, chi2_contingency
import matplotlib.pyplot as plt



from main.utils import write_csv

from main.load_data import load_raw_data


#%% Definitions


def get_top_n_openings(unique_openings_with_counts, n):
    
    unique_openings_with_counts = unique_openings_with_counts.sort_values("count", ascending=False)
    
    top_openings = unique_openings_with_counts.head(n)
    
    return top_openings

#%%
def get_unique_openings_with_counts(df):
    
    
    unique_openings_with_counts =(
        
        df['Opening'].value_counts()
        
                        .reset_index()
                        
                            .sort_values("count", ascending=False)
                                                               
                            )
    
    return unique_openings_with_counts



#%% explore raw data

raw_data = load_raw_data()


unique_openings_from_raw_data = get_unique_openings_with_counts(raw_data)


write_csv(unique_openings_from_raw_data, "unique_openings_from_raw_data.csv")





#%% Load cleaned data
cleaned_data = pd.read_csv("C:/Users/James/OneDrive/Desktop/GitHub/group4_project/cleaned_data.csv")

#%% find uncommon openings


# Step 1: Get all unique openings with their counts
unique_openings_with_counts_from_cleaned_data = get_unique_openings_with_counts(cleaned_data)
    
  
#%% let us define cleaned data that is going through various transformations as the as the following:
    
    
dft = cleaned_data.copy()

#%%


# Step 2: Merge the DataFrames on the 'Opening' column
dft = dft.merge(unique_openings_with_counts_from_cleaned_data, on='Opening', how='left').sort_values("count", ascending=False)

#%%


# Step 3: rename column

dft.rename(columns = {'count':'opening_count'})



#%%



# Calculate the total count
total_count = unique_openings_with_counts_from_cleaned_data['count'].sum()

# Create a new column 'percentage'
unique_openings_with_counts_from_cleaned_data['percentage'] = (unique_openings_with_counts_from_cleaned_data['count'] / total_count) * 100

# Round the percentage to 2 decimal places
unique_openings_with_counts_from_cleaned_data['percentage'] = unique_openings_with_counts_from_cleaned_data['percentage'].round(2)

unique_openings_with_counts_from_cleaned_data = unique_openings_with_counts_from_cleaned_data.sort_values(by='percentage', ascending=False)



#%% Top openings

top_70_openings = get_top_n_openings(unique_openings_with_counts_from_cleaned_data, 70)


top_70_openings.to_csv("top_70_openings.csv")



#%% sort for graphing purposes

unique_openings_with_counts_from_cleaned_data = unique_openings_with_counts_from_cleaned_data.sort_values(by='percentage', ascending=True)


write_csv(unique_openings_with_counts_from_cleaned_data, "unique_openings_with_counts_from_cleaned_data.csv")

#%% plot all openings


# Create the horizontal bar plot
plt.figure(figsize=(10, 8))
plt.barh(unique_openings_with_counts_from_cleaned_data['Opening'], unique_openings_with_counts_from_cleaned_data['percentage'], color='skyblue')

plt.xlabel('Percentage of Games (%)')
plt.title('Chess Openings by Percentage of Games')
plt.grid(axis='x', linestyle='--', alpha=0.7)


plt.tight_layout()

plt.show()




#%%


def plot_top_n_openings_improved(n):
    
    from matplotlib.ticker import MaxNLocator, AutoMinorLocator
    
    top_n_openings = get_top_n_openings(unique_openings_with_counts_from_cleaned_data, n)
    
    # Sort in descending order for better visualization
    top_n_openings = top_n_openings.sort_values(by='percentage', ascending=True)
    
    
    top_n_openings_coverage_percentage = top_n_openings.percentage.sum().round(2)
    
    
    
    # Create the horizontal bar plot
    fig, ax = plt.subplots(figsize=(20, 10))  # figsize = (horizontal,vertical)
    
    
    bars = ax.barh(top_n_openings['Opening'], top_n_openings['percentage'], color='skyblue', align='center')
    
    # Adjust x-axis ticks for better readability
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # Cleaner x-axis numbers
    
    # Add minor ticks to x-axis only
    ax.xaxis.set_minor_locator(AutoMinorLocator(4))  # This adds minor ticks to x-axis
    
    # Add labels and title
    ax.set_xlabel('Percentage of Games (%)', fontsize=12)
    ax.set_title(f'Top {n} Chess Openings by Percentage of Games', fontsize=14, pad=15)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Adjust margins and spacing
    plt.subplots_adjust(left=0.25, right=0.95)  # Reduced left margin
    # Improve spacing and layout
    ax.set_yticks(range(len(top_n_openings)))
    ax.set_yticklabels(top_n_openings['Opening'], fontsize=10)
    
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
plot_top_n_openings_improved(70)

plot_top_n_openings_improved(30)




#%% Top openings

top_30_openings = get_top_n_openings(unique_openings_with_counts_from_cleaned_data, n = 30)


write_csv(top_30_openings, "top_30_openings.csv")


top_30_openings_coverage_percentage = top_30_openings.percentage.sum().round(2)



print(f"\n\nThe top thirty openings account for {top_30_openings_coverage_percentage}% of the total games\n\n")






#%% All games including russian or petrov


opening_name_investigation_from_raw = raw_data[raw_data["Opening"].str.contains("russian", case=False, na=False) |
                                      raw_data["Opening"].str.contains("petrov", case=False, na=False)]




opening_name_investigation_from_raw = get_unique_openings_with_counts(opening_name_investigation_from_raw)


opening_name_investigation_from_clean = cleaned_data[cleaned_data["Opening"].str.contains("russian", case=False, na=False) |
                                      cleaned_data["Opening"].str.contains("petrov", case=False, na=False)]
