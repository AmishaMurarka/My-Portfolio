# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeClassifier as DT
from sklearn.model_selection import train_test_split
import pickle

col_names = ['Area','Perimeter','Compactness','KernelLength','KernelWidth','AsymmeteryCoeff','KernelGrooveLength','KernelType']
data = pd.read_csv(r"C:\Users\Amisha\Desktop\FlaskEnv\FinalProject\static\seeds_dataset.txt",sep = "\s+", names = col_names,index_col=None, engine='python')

X = data.drop('KernelType',axis=1)
y = data['KernelType']

X_train, X_test, y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=1,stratify=y)

kf = KFold(n_splits=10)
# Decision Trees
dt = DT()
dt.fit(X_train,y_train)
print("Score:",dt.score(X_test,y_test))

score_dt = cross_val_score(dt,X,y,cv = kf)
print(score_dt.mean())

with open('model.pkl', 'wb') as file:
    pickle.dump(dt, file)