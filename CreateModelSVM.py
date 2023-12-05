# Load libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split # Import train_test_split function
from joblib import dump
from sklearn import svm
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

col_names = np.load('./vocab/vocab_2023-10-21_20--11--54.npy', allow_pickle=True)
pima = pd.read_excel("./dataset/all/dataset_2023-10-21_20--12--01.xlsx")

class_names=['nghiDinh','nghiQuyet','quyetDinh','thongTu']

#split dataset in features and target variable
feature_cols =col_names[:len(col_names)]
X = pima[col_names] # Features
y = pima.label # Target variable

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # 70% training and 30% test

clf = svm.SVC()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

dump(clf, 'svm_model.pkl')