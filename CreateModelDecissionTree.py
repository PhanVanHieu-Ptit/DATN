# Load libraries
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
from joblib import dump
from datetime import datetime


col_names = np.load('./vocab/vocab_2023-10-28_23--18--36.npy', allow_pickle=True)
pima = pd.read_csv("./dataset/dataset-540/dataset_2023-10-28_23--11--12.csv",encoding='UTF-8')

class_names=['nghiDinh','nghiQuyet','quyetDinh','thongTu']

#split dataset in features and target variable
feature_cols =col_names[:len(col_names)]
X = pima[col_names] # Features
y = pima.label # Target variable

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # 70% training and 30% test

# Create Decision Tree classifer object
clf = DecisionTreeClassifier()

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)


print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

dump(clf, 'decision_tree_model'+ datetime.now().strftime("_%Y-%m-%d_%H--%M--%S.joblib"))

