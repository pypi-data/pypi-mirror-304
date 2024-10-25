#!/usr/bin/env python3
import pandas as pd
from pandas import DataFrame
from typing import Optional, Dict, Union, Tuple
import numpy as np
from dataclasses import dataclass
import fire

@dataclass
class Nsgrads:
    dataset: DataFrame
    periods: int
    column: Optional[str] = None
    edge_order: Optional[int] = 1
    axis: Optional[Union[int, Tuple[int, ...]]] = None

    def get_grads(self) -> Dict:
        if self.column is None:
            print("No column specified. Please provide a column name.")
            return { }
        if self.periods > len(self.dataset):
            print("Values contain NaN. Ensure the number of periods is less than or equal to the length of the dataset.")
        size = pd.DataFrame()
        dfs = []

        try:
            if not self.periods <= 1:
                for i in range(0,self.periods):
                    dfs.append(self.dataset[f'{self.column}'].shift(i))
                new_size = pd.concat(dfs, axis=1)
                cols = []
                for col in range(new_size.shape[1]):
                    cols.append(f'column_{col}')
                new_size.columns = [cols]
                for row in new_size.tail(1).values:
                    grads = np.gradient(list(row), edge_order=self.edge_order, axis=self.axis)
                    mean = grads.mean()
                    result = {
                        'gradients_mean': mean,
                        'gradients': grads,
                        'dataset': new_size.tail(1)
                    }
                    return result
            else:
                print("Periods must be greater than 1!")
        except ValueError as e:
            return {e}


#df = pd.read_csv('./src/ns-gradients/all_sigs_df.csv')
#periods=9
#column = 'close'

def calculator(dataset: DataFrame, periods: int,  column: str):
    try:
        return Nsgrads(dataset=dataset, periods=periods, column=f'{column}').get_grads()
    except Exception as e:
        print(e)



#print(calculator(df,periods,'close').get('dataset'))

#if __name__ == '__main__':
#  calculator()