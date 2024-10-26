import os
import importlib.util
import sys

imp = """
import re
import optuna
import numpy as np
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error, accuracy_score

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier

select,jc,nul,err,t1

import warnings
warnings.filterwarnings("ignore")

known_df = tmp_age_df[tmp_age_df["Age"].notna()]
unknown_df = tmp_age_df[tmp_age_df["Age"].isna()]

known_X = known_df.drop(columns=["Age"])
known_y = known_df["Age"]

model.fit(x_train, y_train)
y_pred = model.predict(x_test)
mse = mean_squared_error(y_test, y_pred)

all_df.loc[all_df["Age"].isna(), "Age"] = unknown_y

test_df.to_csv('datas/test_with_label.csv', index=False)
"""

fselect = """
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold

selector = SelectKBest(f_regression, k=5)
X_train_new = selector.fit_transform(X_train, y_train)
"""

jc = """
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold
model = RandomForestRegressor(n_estimators=100, random_state=42)

kf = KFold(n_splits=5, shuffle=True, random_state=42)

for train_index, test_index in kf.split(X_train):
    X_fold_train, X_fold_test = X_train.iloc[train_index], X_train.iloc[test_index]
    y_fold_train, y_fold_test = y_train.iloc[train_index], y_train.iloc[test_index]

    model.fit(X_fold_train, y_fold_train)
    

classifiers=[]
classifiers.append(SVC())
classifiers.append(DecisionTreeClassifier())
classifiers.append(RandomForestClassifier())
classifiers.append(ExtraTreesClassifier())
classifiers.append(GradientBoostingClassifier())
classifiers.append(KNeighborsClassifier())
classifiers.append(LogisticRegression())
classifiers.append(LinearDiscriminantAnalysis())
    
cv_results=[]
for classifier in classifiers:
    result = cross_val_score(classifier, X, y, scoring="accuracy", cv=5, n_jobs=-1)
    cv_results.append(result)
    
cv_means = []
cv_std = []
cv_name = []
for i, cv_result in enumerate(cv_results):
    cv_means.append(cv_result.mean())
    cv_std.append(cv_result.std())
    cv_name.append(re.match("<method-wrapper '__str__' of (.*?) object at *", str(classifiers[i].__str__)).group(1))
    
cv_res_df = pd.DataFrame({
    "cv_mean": cv_means,
    "cv_std": cv_std,
    "algorithm": cv_name
})

fig = sns.barplot(data=cv_res_df.sort_values(by="cv_mean"), x="cv_mean", y="algorithm", palette="Set1")
fig.set(xlim=(0.7, 0.9))

"""

nul = """
data_without_missing_rows = data.dropna(axis = 0)

column_mean = data['numeric_column'].mean()
data['numeric_column'].fillna(column_mean, inplace = True)

column_median = data['numeric_column'].median()
data['numeric_column'].fillna(column_median, inplace = True)

data['categorical_column'].fillna(data['categorical_column'].mode()[0], inplace = True)

"""

err = """
column_data = data['numeric_column']
mean_value = column_data.mean()
std_value = column_data.std()

lower_bound = mean_value - 3*std_value
upper_bound = mean_value + 3*std_value

outliers = column_data[(column_data < lower_bound) | (column_data > upper_bound)]

data_without_outliers_std = data[~((column_data < lower_bound) | (column_data > upper_bound))]

q1 = column_data.quantile(0.25)
q3 = column_data.quantile(0.75)
iqr = q3 - q1

lower_bound_boxplot = q1 - 1.5*iqr
upper_bound_boxplot = q3 + 1.5*iqr

outliers_boxplot = column_data[(column_data < lower_bound_boxplot) | (column_data > upper_bound_boxplot)]

data_without_outliers_boxplot = data[~((column_data < lower_bound_boxplot) | (column_data > upper_bound_boxplot))]

column_data = np.where(column_data < lower_bound_boxplot, lower_bound_boxplot, column_data)
column_data = np.where(column_data > upper_bound_boxplot, upper_bound_boxplot, column_data)

all_df["Fare"] = all_df["Fare"].map(lambda x: np.log(x) if x > 0 else 0)
"""

t1 = """
ticket_list = []
for ticket, g_df in all_df.groupby("Ticket"):
    ticket_num = g_df["Fare"].shape[0]
    ticket_dict = {
        "Ticket": ticket,
        "EachFare": 0
    }
    if ticket_num > 1:
        if not (g_df["Fare"] == g_df["Fare"].iloc[0]).all():
            ticket_dict["EachFare"] = g_df["Fare"].sum() / ticket_num
        else:
            ticket_dict["EachFare"] = g_df["Fare"].iloc[0] / ticket_num
    else:
        ticket_dict["EachFare"] = g_df["Fare"].iloc[0]
    ticket_list.append(ticket_dict)
ticket_df = pd.DataFrame(ticket_list)
all_df = pd.merge(all_df, ticket_df, on="Ticket")
all_df = all_df.drop(columns=["Fare"]).rename(columns={"EachFare": "Fare"}).sort_values(by="PassengerId")
"""

t2 = """
# 按照TicketNum大小，将TicketNumGroup分为三类。
def ticket_num_group(num):
    if (num >= 2) & (num <= 4):
        return 0
    elif (num == 1) | ((num >= 5) & (num <= 8)):
        return 1
    else:
        return 2
# 得到各位乘客TicketNumGroup的类别
all_df["TicketNumGroup"] = all_df["TicketNum"].map(ticket_num_group)
# 查看TicketNumGroup与Survived之间关系
sns.barplot(data=all_df, x="TicketNumGroup", y="Survived", palette="Set1")
"""



def fimp(pa):
    with open(pa, 'a') as current_file:
        current_file.write(imp)
        
def fselect(pa):
    with open(pa, 'a') as current_file:
        current_file.write(select)
        
def fjc(pa):
    with open(pa, 'a') as current_file:
        current_file.write(jc)
        
def fnul(pa):
    with open(pa, 'a') as current_file:
        current_file.write(nul)
        
def ferr(pa):
    with open(pa, 'a') as current_file:
        current_file.write(err)
           
def ft1(pa):
    with open(pa, 'a') as current_file:
        current_file.write(t1)
        
def ft2(pa):
    with open(pa, 'a') as current_file:
        current_file.write(t2)