import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,confusion_matrix,roc_auc_score

from xgboost import XGBClassifier

from imblearn.over_sampling import SMOTE


# ==============================
# 1 Load Dataset
# ==============================

df = pd.read_excel("data/amazon_churn_dataset_10000.xlsx")

print(df.head())

print(df.info())


# ==============================
# 2 Data Cleaning
# ==============================

print(df.isnull().sum())

df = df.drop_duplicates()


# ==============================
# 3 Exploratory Data Analysis
# ==============================

sns.countplot(x="churn",data=df)
plt.title("Churn Distribution")
plt.show()


sns.histplot(df["age"],bins=20)
plt.title("Age Distribution")
plt.show()


corr = df.corr(numeric_only=True)

sns.heatmap(corr,annot=True,cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()


# ==============================
# 4 Feature Encoding
# ==============================

le = LabelEncoder()

df["region"] = le.fit_transform(df["region"])

df["product_categories"] = le.fit_transform(df["product_categories"])


# ==============================
# 5 Feature Target Split
# ==============================

X = df.drop(["customer_id","churn"],axis=1)

y = df["churn"]


# ==============================
# 6 Train Test Split
# ==============================

X_train,X_test,y_train,y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ==============================
# 7 Handle Class Imbalance
# ==============================

smote = SMOTE(random_state=42)

X_train_smote,y_train_smote = smote.fit_resample(X_train,y_train)


# ==============================
# 8 Logistic Regression
# ==============================

lr = LogisticRegression(max_iter=1000)

lr.fit(X_train_smote,y_train_smote)

pred_lr = lr.predict(X_test)

print("Logistic Regression")

print(confusion_matrix(y_test,pred_lr))

print(classification_report(y_test,pred_lr))


# ==============================
# 9 Random Forest
# ==============================

rf = RandomForestClassifier(n_estimators=200)

rf.fit(X_train_smote,y_train_smote)

pred_rf = rf.predict(X_test)

print("Random Forest")

print(confusion_matrix(y_test,pred_rf))

print(classification_report(y_test,pred_rf))


# ==============================
# 10 XGBoost Model
# ==============================

xgb = XGBClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6
)

xgb.fit(X_train_smote,y_train_smote)

pred_xgb = xgb.predict(X_test)

print("XGBoost")

print(confusion_matrix(y_test,pred_xgb))

print(classification_report(y_test,pred_xgb))


# ==============================
# 11 ROC Score
# ==============================

roc = roc_auc_score(y_test,pred_xgb)

print("ROC Score:",roc)


# ==============================
# 12 Feature Importance
# ==============================

importance = xgb.feature_importances_

features = X.columns

feat_imp = pd.DataFrame({
    "Feature":features,
    "Importance":importance
})

feat_imp = feat_imp.sort_values("Importance",ascending=False)

sns.barplot(x="Importance",y="Feature",data=feat_imp)

plt.title("Feature Importance")

plt.show()


# ==============================
# 13 Predictions
# ==============================

df["predicted_churn"] = xgb.predict(X)

df["churn_probability"] = xgb.predict_proba(X)[:,1]


print(df.head())


# ==============================
# 14 Export for Power BI
# ==============================

df.to_excel("outputs/amazon_churn_powerbi.xlsx",index=False)

print("File exported for Power BI")