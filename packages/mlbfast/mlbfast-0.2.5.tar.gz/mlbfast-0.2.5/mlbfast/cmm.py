import os
import importlib.util
import sys

imp = """
import re
import optuna
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from string import punctuation
from zhon import hanzi
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold
from sklearn.metrics import mean_absolute_error, make_scorer, r2_score, roc_curve, auc, roc_auc_score, f1_score, accuracy_score
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
import warnings
warnings.filterwarnings("ignore")

"""


def imp(pa):
    with open(pa, 'a') as current_file:
        current_file.write(imp)