#%% Adding responsibility into the main dataframe
import pandas as pd
from main.analysis import responsibilities, top_30_openings
from main.analysis import _cleaned_df
from main.analysis import write_csv
import numpy as np

#responsibility look up table (vlookup)
responsibility_lookup = responsibilities.set_index('opening')['responsibility'].to_dict()

_cleaned_df_resp = _cleaned_df.copy()
_cleaned_df_resp['responsibility'] = _cleaned_df_resp['opening'].map(responsibility_lookup)

#print(_cleaned_df_resp.head())

#%% Dropping columns where responsibility is nan
_cleaned_df_resp_wo_nan = _cleaned_df_resp.dropna(subset=['responsibility'])

#%% Adding responsibility
#rarity_df = pd.read_csv('C:\\Users\\annaz\\Desktop\\PDA in Data Science\\Data Science Project\\data\\top_30_openings_rarity_incl.csv')

rarity_df = pd.merge(_cleaned_df_resp_wo_nan, top_30_openings, how = "left",  on = "opening")
rarity_lookup = rarity_df.set_index('opening')['rarity'].to_dict()
_cleaned_df_resp_wo_nan['rarity'] = _cleaned_df_resp['opening'].map(rarity_lookup)

#%% Adding game outcome
_cleaned_df_resp_wo_nan['outcome'] = np.where(
    (_cleaned_df_resp_wo_nan['responsibility'] == 'white') & (_cleaned_df_resp_wo_nan['result'] == '1-0') |
    (_cleaned_df_resp_wo_nan['responsibility'] == 'black') & (_cleaned_df_resp_wo_nan['result'] == '0-1'),
    'won',
    'lost')

write_csv(_cleaned_df_resp_wo_nan, "cleaned_df_updated.csv" )

#%% Chi-squared test of independence
#To see if the game outcome and the chosen outcome is related

outcome_count_table = pd.crosstab(
    _cleaned_df_resp_wo_nan['outcome'],
    _cleaned_df_resp_wo_nan['rarity'],
    margins = True,
    margins_name = "total")

print(outcome_count_table)

from scipy.stats import chi2_contingency

contingency_data = [[7078, 2200], [7016, 1920]]
stat, p, dof, expected = chi2_contingency(contingency_data)

# interpret p-value
alpha = 0.05
print("p value is " + str(p))
if p <= alpha:
    print('Dependent (reject H0)')
else:
    print('Independent (H0 holds true)')


#%% Logistic regression
#To try and predict game outcome based on chosen opening

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import label_binarize

X_raw = _cleaned_df_resp_wo_nan['rarity']
Y_outcome = np.array(_cleaned_df_resp_wo_nan['outcome'])

X_rarity = label_binarize(X_raw, classes=['common', 'uncommon']) # common 0, uncommon 1

logr = LogisticRegression()
logr.fit(X_rarity, Y_outcome)

predicted = logr.predict(np.array([0]).reshape(-1,1))
print(predicted)

#%% Naive Bayes
#Mini machine learning algorithm to calculate the probability of winning when using a certain opening
#and playing a certain colour



