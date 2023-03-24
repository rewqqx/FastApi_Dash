import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


from sklearn.model_selection import train_test_split


from sklearn.metrics import confusion_matrix, classification_report

from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier

import joblib
joblib_file = "joblib_model.pkl"

model = joblib.load(joblib_file)
plt.barh(model.feature_names_in_, model.feature_importances_)
plt.show()
