'''
@file    : DataExploration.py
@time    : Feb 24,2016 13:28
@author  : duanxxnj@163.com
'''

import pandas as pd
import numpy as np
from scipy.stats import mode

#Read files:
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

print type(train)
print type(test)

train['source'] = 'train'
test['source'] = 'test'

data = pd.concat([train, test], ignore_index=True)

print train.shape, test.shape, data.shape

print data.apply(lambda x: sum(x.isnull()))

print data.dtypes

print data.describe()

print data.apply(lambda x: len(x.unique()))

categorical_columns = [x for x in data.dtypes.index if data.dtypes[x]=='object']

categorical_columns = [x for x in categorical_columns
                       if x not in ['Item_Identifier',
                                    'Outlet_Identifier',
                                    'source']]

for col in categorical_columns:
    print '\n Frequency of Categories fro varible : ', col
    print data[col].value_counts()


item_avg_weight = data.pivot_table(values='Item_Weight',
                                   index='Item_Identifier')

miss_bool = data['Item_Weight'].isnull()

print 'Orignal #missing', sum(miss_bool)

data.loc[miss_bool, 'Item_Weight'] = \
    data.loc[miss_bool, 'Item_Identifier'].\
        apply(lambda x: item_avg_weight[x])

print 'Final #missing', sum(data['Item_Weight'].isnull())

outlet_size_mode = data.pivot_table(values='Outlet_Size',
                                    columns='Outlet_Type',
                                    aggfunc=(lambda x:mode(x).mode[0]))

miss_bool = data['Outlet_Size'].isnull()

print 'Original #missing', sum(miss_bool)

data.loc[miss_bool, 'Outlet_Size'] = data.loc[miss_bool, 'Outlet_Type'].\
    apply(lambda x: outlet_size_mode[x])

print 'Final #missing', sum(data['Outlet_Size'].isnull())

print data.pivot_table(values='Item_Outlet_Sales', index='Outlet_Type')


visibility_avg = data.pivot_table(values='Item_Visibility',
                                  index='Item_Identifier')

miss_bool = (data['Item_Visibility'] == 0)

print 'Number of 0 values initially: ', sum(miss_bool)

data.loc[miss_bool, 'Item_Visibility'] =\
    data.loc[miss_bool, 'Item_Identifier'].\
        apply(lambda x: visibility_avg[x])

print 'Number of 0 values afer modification:', sum(data['Item_Visibility'] == 0)

data['Item_Visibility_MeanRatio'] =\
    data.apply(lambda x: x['Item_Visibility']/
                         visibility_avg[x['Item_Identifier']], axis=1)

print data['Item_Visibility_MeanRatio'].describe()

data['Item_Identifier'].value_counts()

data['Item_Type_Combined'] = data['Item_Identifier'].apply(lambda x: x[0:2])

data['Item_Type_Combined'].value_counts()

data['Outlet_Years'] = 2013 - data['Outlet_Establishment_Year']
data['Outlet_Years'].describe()

data['Item_Fat_Content'].value_counts()

data['Item_Fat_Content'] = data['Item_Fat_Content'].\
    replace({'LF': 'Low Fat',
             'reg': 'Regular',
             'low fat': 'Low Fat'})

data['Item_Fat_Content'].value_counts()

