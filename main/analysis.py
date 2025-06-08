import pandas as pd
from scipy.stats import binomtest, chi2_contingency
import matplotlib.pyplot as plt


import seaborn as sns

import statsmodels.api as sm

from statsmodels.api import Logit, add_constant



from main.utils import write_csv, read_csv

from main.load_data import load_raw_data


import pprint as pretty


from main.cleaning import make_all_col_names_lowercase

from main.utils import view_df as view


import numpy as np



_show_graphs = True

_analysis = True

_debug = True


#%% Definitions


def get_top_n_openings(unique_openings_with_counts, n):
    
    unique_openings_with_counts = make_all_col_names_lowercase(unique_openings_with_counts)
    
    unique_openings_with_counts = unique_openings_with_counts.sort_values("count", ascending=False)
    
    top_openings = unique_openings_with_counts.head(n)
    
    return top_openings

#%%
def get_unique_openings_with_counts(dft):
    
    
    dft = make_all_col_names_lowercase(dft)
    
    unique_openings_with_counts =(
        
        dft['opening'].value_counts()
        
                        .reset_index()
                        
                            .sort_values("count", ascending=False)
                                                               
                            )
    
    
    
    return unique_openings_with_counts



#%% add_rarity_column

def add_rarity_column(dft, pct_threshold: float = 2.0):
    
    
    """
    Adds a 'rarity' column with values 'common' or 'uncommon',
    based on whether the opening's percentage is above or below the threshold.

    """
    
    dft["rarity"] = dft["%_of_all_openings_played"].apply(
        
        lambda p: "uncommon" if p < pct_threshold else "common"
    )
    return dft

#%%

def get_outcome(row):
    
    if row['responsibility'] == 'white':
        
        return 'won' if row['result'] == '1-0' else 'lost'
    
    
    
    elif row['responsibility'] == 'black':
        
        return 'won' if row['result'] == '0-1' else 'lost'
    
    

    else:
        raise ValueError(f"Unexpected responsibility value")



#%%



def rarity_outcome_by_cap(dft, cap=None):
    """Return counts, win-rates, χ² statistic, p-value, and cap after filtering on abs(elo_difference) <= cap."""

    subset = dft.loc[dft['elo_difference'].abs() <= cap].copy()

    # outcome for the responsible player ------------------------------
    subset['won'] = (
        (subset['responsibility'] == 'white') & (subset['result'] == '1-0')
        | (subset['responsibility'] == 'black') & (subset['result'] == '0-1')
    )

    crosstab = pd.crosstab(subset['won'], subset['rarity'])

    # χ² test of independence (common vs uncommon, win vs loss)
    chi2, p, _, _ = chi2_contingency(crosstab.values, correction=False)

    summary = crosstab.rename(index={False: 'lost', True: 'won'})
    summary['row_total'] = summary.sum(1)
    summary.loc['col_total'] = summary.sum(0)

    win_rates = (summary.loc['won', ['common', 'uncommon']]
                 / summary.loc['col_total', ['common', 'uncommon']])

    return summary, win_rates, chi2, p, cap




#%% explore raw data

RAW_DATA = load_raw_data()


unique_openings_from_raw_data = get_unique_openings_with_counts(RAW_DATA)


write_csv(unique_openings_from_raw_data, "unique_openings_from_raw_data.csv")





#%% Load cleaned data
_cleaned_df = read_csv("cleaned_df.csv")

#%% find uncommon openings


# Step 1: Get all unique openings with their counts
unique_openings_with_counts_from_cleaned_df = get_unique_openings_with_counts(_cleaned_df)
    
  
#%% let us define cleaned data that is going through various transformations as the as the following:
    
    
dft = _cleaned_df.copy()

#%%


# Step 2: Merge the DataFrames on the 'opening' column

dft = dft.merge(unique_openings_with_counts_from_cleaned_df, on='opening', how='left').sort_values("count", ascending=False).reset_index(drop = True)

#%%


# Step 3: rename column

dft = dft.rename(columns = {'count':'opening_count'})




#%%



# Calculate the total opening_count
total_count = unique_openings_with_counts_from_cleaned_df['count'].sum()

# Create a new column 'percentage'
unique_openings_with_counts_from_cleaned_df['percentage'] = (unique_openings_with_counts_from_cleaned_df['count'] / total_count) * 100


# verify that the percentage column sums to one

percentage_verification = sum(unique_openings_with_counts_from_cleaned_df.percentage)




# Round the percentage to 2 decimal places
unique_openings_with_counts_from_cleaned_df['percentage'] = unique_openings_with_counts_from_cleaned_df['percentage'].round(2)

unique_openings_with_counts_from_cleaned_df = unique_openings_with_counts_from_cleaned_df.sort_values(by='percentage', ascending=False)



#%% Top openings

top_70_openings = get_top_n_openings(unique_openings_with_counts_from_cleaned_df, 70)


top_70_openings.to_csv("top_70_openings.csv")



#%% sort for graphing purposes

unique_openings_with_counts_from_cleaned_df = unique_openings_with_counts_from_cleaned_df.sort_values(by='percentage', ascending=True)


write_csv(unique_openings_with_counts_from_cleaned_df, "unique_openings_with_counts_from_cleaned_dft.csv")

#%% plot all openings

if _show_graphs:
    
    
    # Create the horizontal bar plot
    plt.figure(figsize=(10, 8))
    plt.barh(unique_openings_with_counts_from_cleaned_df['opening'], unique_openings_with_counts_from_cleaned_df['percentage'], color='skyblue')
    
    plt.xlabel('Percentage of Games (%)')
    plt.title('Chess openings by Percentage of Games')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    
    plt.tight_layout()
    
    plt.show()
    
    
    

#%%


def plot_top_n_openings(n):
    
    from matplotlib.ticker import MaxNLocator, AutoMinorLocator
    
    top_n_openings = get_top_n_openings(unique_openings_with_counts_from_cleaned_df, n)
    
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
    
    
    


if _show_graphs:
    
    plot_top_n_openings(70)
    
    plot_top_n_openings(30)




#%% Top openings

top_30_openings = get_top_n_openings(unique_openings_with_counts_from_cleaned_df, n = 30)


write_csv(top_30_openings, "top_30_openings.csv")


top_30_openings_coverage_percentage = top_30_openings.percentage.sum().round(2)


if _analysis:
    print(f"\n\nThe top thirty openings account for {top_30_openings_coverage_percentage}% of the total games\n\n")






#%%  Begining an investigation of strangeness in opening names

#

"""
I noticed that the Petrov Defense fell outside the top thirty openings.

I thought this was unusual given that it is a well-established and frequently

played opening at the highest levels of chess.

To investigate, I began by reviewing the unique openings present in our dataset.

I observed that several different names referred to the same opening:

- 'Russian Game'
- 'Petrov's Defense'
- 'Petrov'

These are all aliases for the same opening—the Petrov Defense—and should be treated as such for accurate statistical analysis. The inconsistency in naming likely led to a fragmentation of data, artificially lowering its apparent popularity.

To address this, I added a standardization step to the data cleaning pipeline that maps these variants to a single consistent name: 'Petrov'.


"""

opening_name_investigation_from_clean = _cleaned_df[_cleaned_df["opening"].str.contains("russian", case=False, na=False) |
                                      _cleaned_df["opening"].str.contains("petrov", case=False, na=False)]



opening_name_investigation_from_clean = get_unique_openings_with_counts(opening_name_investigation_from_clean)



############




opening_name_investigation_from_raw = RAW_DATA[RAW_DATA["opening"].str.contains("russian", case=False, na=False) |
                                      RAW_DATA["opening"].str.contains("petrov", case=False, na=False)]




opening_name_investigation_from_raw = get_unique_openings_with_counts(opening_name_investigation_from_raw)



#%% write to file in data folder

# compare with files of the same name in saved data for evidence
# to see that cleaning has been successful



write_csv(opening_name_investigation_from_raw, "opening_name_investigation_from_raw.csv" )

write_csv(opening_name_investigation_from_clean, "opening_name_investigation_from_clean.csv" )



#%% classify top 30


if _debug:

    
    # Assuming top_30_openings is a DataFrame with an "opening" column
    responsibilities = [(opening, '') for opening in top_30_openings["opening"]]
    
    pretty.pprint(responsibilities)
    
    
    print("\n\n\n")

    
    
    
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
        
        
        ('English Opening', 'white'),
        
        ("Bishop's Opening", 'white'),
        
        
        ('Caro-Kann Defense', 'black'),
        
        ('Scotch Game', 'white'),
        
        ('Four Knights Game', 'white'),
        
        ("Van't Kruijs Opening", 'white'),
        
        ("Queen's Gambit Declined", 'black'),
        
        ("Queen's Gambit Accepted", 'black'),
        
        
        
        ('Petrov', 'black'), # This entered the top thirty
                             # after additional cleaning
                             
                             
        
        ('Modern Defense', 'black'),
        
        ('Nimzowitsch Defense', 'black'),
        
        ('Indian Game', 'black'),
        
        ("Queen's Gambit Refused", 'black'),
        
        ('Horwitz Defense', 'black'),
        
        ('Pirc Defense', 'black'),
        
        ("King's Knight Opening", 'white'),
        
        ('Center Game', 'white'),
        
        
        
        
        ('Vienna Game', 'white'),
        
        ('Owen Defense', 'black'),
        
        ('Hungarian Opening', 'white'),
        
        ('Slav Defense', 'black'),
        
        #('Alekhine Defense', 'black'),
        
        ('Three Knights Opening', 'white'), 
]


responsibilities = pd.DataFrame(responsibilities)


responsibilities = responsibilities.rename(columns= { 
    
                                                     0: "opening",
                                           
                                                     
                                                     1: "responsibility" 
                                                     
                                                     }
                                           )



#%% add responsibilities to dft

dft = pd.merge(dft, responsibilities, how = "left", on = "opening")



top_30_openings_for_merge = top_30_openings[["opening", "percentage"]]


top_30_openings_for_merge = top_30_openings_for_merge.rename(
    columns={"percentage": "%_of_all_openings_played"}
)


dft = pd.merge(top_30_openings_for_merge, dft, how = "left", on = "opening")







#%% conclusion of petrov alias name issue

"""

After we investigated the Petrov alias name issue

and renamed the aliases to be uniform we found that the Petrov,

which was previously outside the top thirty most played openings

jumped up to 17th place on the most played. 


And knocked the Alekhine Defense Opening out of the list altogether. 


"""


#%% add in absolute elo difference

# This is not greater than 200 points

# made sure of this at the conversion stage

# N.B. don't mix up with rating diff -- which is how much a rating
#      changes after the conclusion of a game



#%% Calculate and insert elo difference column

elo_difference = (dft["blackelo"] - dft["whiteelo"]).abs()


dft.insert(
    
    dft.columns.get_loc("blackelo") + 1,
    
    "elo_difference",
    
    elo_difference)


del elo_difference

#%% add in rarity column


dft = add_rarity_column(dft)  # default threshold is 2%


dft['outcome_for_responsible_player'] = np.where(
    (dft['responsibility'] == 'white') & (dft['result'] == '1-0') |
    (dft['responsibility'] == 'black') & (dft['result'] == '0-1'),
    'won',
    'lost')


#%% checking

dft['outcome_for_responsible_player_2'] = dft.apply(get_outcome, axis=1)


if _debug:
    
    print ("\n\n")
    
    print ("The columns are equal:")
    
    print(
        
        dft['outcome_for_responsible_player']
        
        .equals(dft['outcome_for_responsible_player_2'])
        
        )
    
    
    
dft = dft.drop(columns = ['outcome_for_responsible_player_2'])


#%% add in cross table


outcome_count_table = pd.crosstab(
    dft['outcome_for_responsible_player'],
    dft['rarity'],
    margins = True,
    margins_name = "total").reset_index()


#%%

summary, win_rates, chi2, p, cap = rarity_outcome_by_cap(dft, cap =200)

print("\n")
print("cap = " + str(cap) + "\n")
print(summary)
print("\nWin-rates  |  common: {:.2%}   uncommon: {:.2%}".format(*win_rates))
print("χ² statistic: {:.4f}".format(chi2))
print("χ² p-value:", p)




#%% Data Preparation
# Copy the original DataFrame
dft = dft.copy()

# Convert outcome to binary (1 = won, 0 = lost)
dft['won'] = (dft['outcome_for_responsible_player'] == 'won').astype(int)

# Convert 'rarity' to binary (0 = common, 1 = uncommon)
dft['rarity_binary'] = (dft['rarity'] == 'uncommon').astype(int)

# Define predictors and response
X = add_constant(dft[['rarity_binary', 'elo_difference']])
y = dft['won']

#%% Fit Logistic Regression Model

# Logit(p) = log(p / (1 - p))


model = Logit(y, X).fit()
print(model.summary())

#%% Plot 1: Win Rate by Opening Rarity
plt.figure(figsize=(8, 5))
sns.stripplot(x='rarity', y='won', data=dft, jitter=True, alpha=0.3)
sns.pointplot(x='rarity', y='won', data=dft, estimator=np.mean, color='red', markers='o')
plt.title("Win Rate by Opening Rarity")
plt.ylabel("Win (1) / Loss (0)")
plt.xlabel("Opening Rarity")
plt.show()

#%% Plot 2: Predicted Win Probability by Elo Difference and Rarity
# Predict probabilities using the model
dft['pred_prob'] = model.predict(X)

# Scatter plot of predicted probabilities
plt.figure(figsize=(8, 5))
sns.scatterplot(
    x='elo_difference',
    y='pred_prob',
    hue='rarity_binary',
    data=dft.sample(1000),  # downsample for clarity
    alpha=0.4
)
plt.title("Predicted Win Probability by Elo Difference and Rarity")
plt.ylabel("Predicted Win Probability")
plt.xlabel("Elo Difference")
plt.legend(title='Uncommon Opening?')
plt.show()







#experimental

#%% Parameters ---------------------------------------------------------------
USE_ELO = False          # set to True if you want to include elo_difference

#%% Data preparation ---------------------------------------------------------
dft = dft.copy()
dft['won']           = (dft['outcome_for_responsible_player'] == 'won').astype(int)
dft['rarity_binary'] = (dft['rarity'] == 'uncommon').astype(int)

# Choose predictors based on the flag
predictors = ['rarity_binary']
if USE_ELO:
    predictors.append('elo_difference')

# Design matrix
X = add_constant(dft[predictors])
y = dft['won']

#%% Fit logistic model -------------------------------------------------------
model = Logit(y, X).fit()

print(model.summary())

#%% (Optional) Likelihood-ratio test if Elo is available ---------------------
if USE_ELO:
    # Fit the nested model without Elo for comparison
    X_no_elo   = add_constant(dft[['rarity_binary']])
    model_base = Logit(y, X_no_elo).fit(disp=0)   # suppress extra output
    
    from scipy.stats import chi2
    lr_stat = 2 * (model.llf - model_base.llf)
    lr_p    = chi2.sf(lr_stat, dft=1)
    
    print(f"\nLR test for Elo term → χ² = {lr_stat:.3f} (dft = 1), p = {lr_p:.4f}")
    
    
    
#%% export key data frames to csv


write_csv(dft, "transformed_data.csv")

write_csv(outcome_count_table, "outcome_count_table.csv")

write_csv(top_30_openings, "top_30_openings.csv")

write_csv(win_rates, "win_rates.csv")
