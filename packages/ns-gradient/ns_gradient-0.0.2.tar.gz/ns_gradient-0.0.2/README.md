# ns_gradient
This package is used to calculate the gradients of a shifted column of dataset to form a rows  

```
  column_0 column_1 column_2 column_3 column_4 column_5
0  0.05601      NaN      NaN      NaN      NaN      NaN
1  0.08611  0.05601      NaN      NaN      NaN      NaN
2  0.05125  0.08611  0.05601      NaN      NaN      NaN
3  0.02576  0.05125  0.08611  0.05601      NaN      NaN
4  0.01776  0.02576  0.05125  0.08611  0.05601      NaN
```
## Usage
Once installed ns_gradient can be imported and functions called like so:  

```
import pandas as pd
from ns_gradient.nsgrads import Nsgrads, calculator
df = pd.read_csv('./src/ns_gradient/all_sigs_df.csv')
df.drop(['Unnamed: 0'], axis=1, inplace=True)

result = calculator(dataset=df, periods=20, column='close')

print(result.get('gradients_mean')) # to get the mean
print(result.get('dataset')) # to retrieve data used to calculate the gradients
print(result.get('gradients')) # to get the vector gradients
```

