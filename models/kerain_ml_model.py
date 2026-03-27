import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# =====================================
# LOAD DATA
# =====================================

data = pd.read_csv("kerain_multiregion_data.csv")

print("\nDataset Loaded Successfully ✅")
print("Total Samples:", len(data))

print("\nClass Distribution:")
print(data["flood"].value_counts())

# Features and target
X = data.drop(["flood"], axis=1)
y = data["flood"]

# =====================================
# MODEL INITIALIZATION
# =====================================

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    random_state=42
)

# =====================================
# STRATIFIED CROSS VALIDATION
# =====================================

print("\n==============================")
print("STRATIFIED CROSS VALIDATION")
print("==============================")

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(model, X, y, cv=skf)

print("CV Scores:", cv_scores)
print("Average CV Score:", round(cv_scores.mean(), 4))

# =====================================
# TRAIN / TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

model.fit(X_train, y_train)

# =====================================
# EVALUATION
# =====================================

print("\n==============================")
print("TEST SET EVALUATION")
print("==============================")

y_pred = model.predict(X_test)

train_acc = model.score(X_train, y_train)
test_acc = accuracy_score(y_test, y_pred)

print("Training Accuracy:", round(train_acc, 4))
print("Test Accuracy:", round(test_acc, 4))

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)

print("Confusion Matrix:")
print(cm)

# =====================================
# FEATURE IMPORTANCE
# =====================================

feature_importance = pd.Series(
    model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

print("\nFeature Importance:\n")
print(feature_importance)

# =====================================
# CONFUSION MATRIX PLOT
# =====================================

plt.figure()
plt.imshow(cm)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.colorbar()

for i in range(len(cm)):
    for j in range(len(cm)):
        plt.text(j, i, cm[i, j], ha='center', va='center')

plt.show()