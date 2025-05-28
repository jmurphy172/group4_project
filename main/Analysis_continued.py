#Adding responsibility into the main dataframe
import pandas as pd
from main.analysis import responsibilities
from main.analysis import _cleaned_df
from main.analysis import write_csv
import numpy as np

from main.paths import get_data_path

#%% responsibility look up table (vlookup)


responsibility_lookup = responsibilities.set_index('opening')['responsibility'].to_dict()


#%% Add responsibility into 

cleaned_df_resp = _cleaned_df.copy()

cleaned_df_resp['responsibility'] = cleaned_df_resp['opening'].map(responsibility_lookup)

#%% 

# print(cleaned_df_resp.head())

#%% dropping columns where responsibility is nan
cleaned_df_resp_wo_nan = cleaned_df_resp.dropna(subset=['responsibility'])




#%%

# set data path

data_path =  get_data_path()


rarity_df = rare_openings = pd.read_csv(data_path / "top_30_openings_rarity_incl.csv")

#%%




rarity_lookup = rarity_df.set_index('opening')['rarity'].to_dict()
cleaned_df_resp_wo_nan['rarity'] = cleaned_df_resp['opening'].map(rarity_lookup)

#game outcome
cleaned_df_resp_wo_nan['outcome'] = np.where(
    (cleaned_df_resp_wo_nan['responsibility'] == 'white') & (cleaned_df_resp_wo_nan['result'] == '1-0') |
    (cleaned_df_resp_wo_nan['responsibility'] == 'black') & (cleaned_df_resp_wo_nan['result'] == '0-1'),
    'won',
    'lost')

write_csv(cleaned_df_resp_wo_nan, "cleaned_df_updated.csv" )

outcome_count_table = pd.crosstab(
    cleaned_df_resp_wo_nan['outcome'],
    cleaned_df_resp_wo_nan['rarity'],
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


#Logistic regression
#import scikit-learn as sklearn
#from sklearn import linear_model

#X_rarity = numpy.array(cleaned_df_resp_wo_nan['rarity'])
#Y_outcome = numpy.array(cleaned_df_resp_wo_nan['outcome'])

#logr = linear_model.LogisticRegression()
#logr.fit(X_rarity,Y_outcome)

#predicted = logr.predict(numpy.array([common]).reshape(-1,1))
#print(predicted)