import pandas as pd
#from nsgrads import Nsgrads, calculator

from ns_gradient.nsgrads import Nsgrads, calculator
df = pd.read_csv('./src/ns_gradient/all_sigs_df.csv')
df.drop(['Unnamed: 0'], axis=1, inplace=True)
#print(df.columns)

result = calculator(dataset=df, periods=20, column='close')

print(result.get('gradients_mean'))
