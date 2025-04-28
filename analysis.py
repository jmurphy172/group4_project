import pandas as pd
from scipy.stats import binomtest, chi2_contingency

# Load cleaned data
df = pd.read_csv("C:/Users/James/OneDrive/Desktop/GitHub/group4_project/cleaned_data.csv")

#%% find uncommon openings


# Step 1: Get all unique openings with their counts
unique_openings_with_counts = df['Opening'].value_counts()

# Step 2: Convert to a DataFrame for better visualization
unique_openings_df = unique_openings_with_counts.reset_index()
unique_openings_df.columns = ['Opening', 'Count']

# Step 3: Display the result
print(unique_openings_df)

# Step 4 (Optional): Save the unique openings with counts to a CSV file
unique_openings_df.to_csv("unique_openings_with_counts.csv", index=False)

# Step 5: Display summary of counts for each category
print(df['Opening_Type'].value_counts())



#%%


# Step 1: Merge the DataFrames on the 'Opening' column
merged_df = df.merge(unique_openings_df, on='Opening', how='left')

# Step 2: Verify the result
print(merged_df.head())

# Step 3 (Optional): Save the merged DataFrame to a CSV file
merged_df.to_csv("merged_games_with_counts.csv", index=False)




