# -*- coding: utf-8 -*-

# Import the required libraries 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

# Load dataset

df=pd.read_csv('/content/sample_data/heart.csv')

"""# Data Preprocessing

<span style='font-size:20px; color: blue'><b>Data Visualization and Cleaning</b></span>
"""

df.head()

df.info()

"""<span style='font-size:20px'>Checking for Missing Values</span>"""

df.isnull().sum()

"""<span style='font-size:20px'>Checking for Duplicated Rows</span>"""

# Count the number of duplicated rows
num_duplicates = df.duplicated().sum()

# Print the number of duplicated rows
print(f"Number of duplicated rows: {num_duplicates}")

"""<span style='font-size:20px'>Handle duplicated rows</span>"""

# Keep only the first occurrence of duplicated rows
df = df.drop_duplicates()
#confirm if data duplication have been handled
df.duplicated().any()

"""<span style='font-size:20px'>**Correlation**</span>

useful for understanding the relationships between different variables in your dataset. It helps in identifying highly correlated variables, which can have implications for feature selection and gaining insights into the underlying patterns in the data.
"""

# Calculate the correlation coefficient matrix
correlation_matrix = df.corr()

# Plot the correlation matrix
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title("Correlation Matrix")
plt.show()

"""*   1 indicates a perfect positive linear relationship (both variables increase together).
*   -1 indicates a perfect negative linear relationship (one variable increases while the other decreases together).
*   0 indicates no linear relationship (the variables are not correlated).

RESULTS OF THE PREDICTED MODEL BEFORE REMOVING
EXTREME OUTLIERS
"""

X = df.drop('target', axis=1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Initialize the model
model = GradientBoostingClassifier()

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Calculate the confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred)

# Calculate the precision
precision = precision_score(y_test, y_pred)

# Calculate the recall
recall = recall_score(y_test, y_pred)

# Calculate the F1 score
f1 = f1_score(y_test, y_pred)

# Print the confusion matrix
print("Confusion Matrix:")
print(cm)

# Print the accuracy
print("Accuracy:", accuracy)

# Print the precision
print("Precision:", precision)

# Print the recall
print("Recall:", recall)

# Print the F1 score
print("F1 Score:", f1)
# Plot the confusion matrix
plt.figure(figsize=(6, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

"""<span style='font-size:20px; color:blue'><b>Checking For Outliers</b></span>

performing outlier detection and removal using the Interquartile Range (IQR) method.
Data points that fall above the upper threshold or below the lower threshold are considered extreme outliers.
"""

# Calculate the IQR for each column
Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1

# Determine the threshold for extreme outliers
upper_threshold = Q3 + 3 * IQR
lower_threshold = Q1 - 3 * IQR

# Remove extreme outliers
df_filtered = df[((df >= lower_threshold) & (df <= upper_threshold)).all(axis=1)]

# Calculate the number of removed instances
removed_instances = len(df) - len(df_filtered)

# Print the filtered DataFrame
print("Filtered DataFrame:")
print(df_filtered)
print()

# Print the number of removed instances
print(f"Number of removed instances: {removed_instances}")

"""RESULTS OF THE PREDICTED MODEL AFTER REMOVING
EXTREME OUTLIERS
"""

X = df_filtered .drop('target', axis=1)
y = df_filtered ['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Initialize the model
model = GradientBoostingClassifier()

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Calculate the confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred)

# Calculate the precision
precision = precision_score(y_test, y_pred)

# Calculate the recall
recall = recall_score(y_test, y_pred)

# Calculate the F1 score
f1 = f1_score(y_test, y_pred)

# Print the confusion matrix
print("Confusion Matrix:")
print(cm)

# Print the accuracy
print("Accuracy:", accuracy)

# Print the precision
print("Precision:", precision)

# Print the recall
print("Recall:", recall)

# Print the F1 score
print("F1 Score:", f1)

# Plot the confusion matrix
plt.figure(figsize=(6, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

"""<span style='font-size:20px; color: blue'><b>Checking for Imbalances</b></span>

imbalanced data can introduce bias into the predictive models
When one class is significantly more prevalent than the other, the model may become biased towards the majority class, leading to poor performance in predicting the minority class
"""

# Count the occurrences of each category
category_counts = df_filtered ['target'].value_counts()

# Calculate the balance ratio
balance_ratio = category_counts[0] / category_counts[1]

# Plot the category counts
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='target')
plt.title("Output Balance")
plt.xlabel("Target")
plt.ylabel("Count")
plt.show()

# Print the balance ratio
print(f"Balance ratio: {balance_ratio:.2f}")

"""majority class has approximately 0.83 times more samples than the minority class

<span style='font-size:20px'>**Data Resampling**</span>

used to handle imbalanced datasets
"""

# Count the occurrences of each category
category_counts = df['target'].value_counts()

# Calculate the original balance ratio
original_balance_ratio = category_counts[0] / category_counts[1]

# Resample the data to balance the classes
resampled_data = df.groupby('target', as_index=False).apply(lambda x: x.sample(n=category_counts.min(), replace=True)).reset_index(drop=True)

# Count the occurrences of each category in the resampled data
resampled_category_counts = resampled_data['target'].value_counts()

# Calculate the resampled balance ratio
resampled_balance_ratio = resampled_category_counts[0] / resampled_category_counts[1]

# Print the resampled balance ratio
print(f"Resampled Balance ratio: {resampled_balance_ratio:.2f}")

"""<span style='font-size:20px; color:blue'><b>Feature selectiong</b></span>

RFECV is a feature selection method that recursively removes less important features and selects the most important ones based on cross-validated performance.
StratifiedKFold ensures that each fold in the cross-validation retains the same class distribution as the original dataset, which is essential when dealing with imbalanced datasets.
"""

from sklearn.feature_selection import RFECV

from sklearn.model_selection import StratifiedKFold
# Separate features and target variable
X = resampled_data.drop('target', axis=1)
y = resampled_data['target']

# Initialize the model for feature selection
estimator = GradientBoostingClassifier()

# Initialize RFECV with the estimator and cross-validation strategy
rfecv = RFECV(estimator=estimator, cv=StratifiedKFold())

# Fit RFECV on the data
rfecv.fit(X, y)

# Get the optimal number of features
optimal_num_features = rfecv.n_features_

# Get the selected features
selected_features = X.columns[rfecv.support_]

# Print the optimal number of features
print("Optimal Number of Features:", optimal_num_features)

# Print the selected features
print("Selected Features:")
print(selected_features)

X=resampled_data[['cp', 'chol', 'thalach', 'oldpeak', 'ca', 'thal']]
y=resampled_data['target']

"""<span style='font-size:20px; color:blue'><b>Data Splitting</b></span>"""

# Split the data into training and testing sets

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

"""# Applied Algorithm"""

# Initialize the model
model = GradientBoostingClassifier()

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)
y_pred

"""RESULTS OF THE PREDICTED MODEL AFTER APPLYING
FEATURE SELECTION

# Model Evaluation
"""

from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
# Calculate the confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred)

# Calculate the precision
precision = precision_score(y_test, y_pred)

# Calculate the recall
recall = recall_score(y_test, y_pred)

# Calculate the F1 score
f1 = f1_score(y_test, y_pred)

# Print the confusion matrix
print("Confusion Matrix:")
print(cm)

# Print the accuracy
print("Accuracy:", accuracy)

# Print the precision
print("Precision:", precision)

# Print the recall
print("Recall:", recall)

# Print the F1 score
print("F1 Score:", f1)
# Plot the confusion matrix
plt.figure(figsize=(6, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

"""confusion matrix:
*  25 instances were correctly predicted as Class 0 (true negatives).
*  5 instances were incorrectly predicted as Class 1, but they actually belong to Class 0 (false positives or Type I errors).
*  2 instances were incorrectly predicted as Class 0, but they actually belong to Class 1 (false negatives or Type II errors).
*  24 instances were correctly predicted as Class 1 (true positives).

Accuracy measures the proportion of correctly classified instances out of the total instances in the dataset.
*   model achieved an accuracy of 0.875, which means approximately 87.5% of the instances were correctly classified.

Precision, also known as positive predictive value, measures the proportion of true positive predictions out of all positive predictions made by the model.
*   model achieved a precision of approximately 82.76%, indicating that when it predicted an instance to belong to the positive class, it was correct about 82.76% of the time.

Recall, also known as sensitivity or true positive rate, measures the proportion of true positive predictions out of all actual positive instances in the dataset.
*   model achieved a recall of approximately 92.31%, indicating that it correctly identified 92.31% of the actual positive instances in the dataset.

F1 score is the harmonic mean of precision and recall and provides a balanced measure of the model's performance that takes both false positives and false negatives into account.
*   F1 score is approximately 87.27%, indicating a good balance between precision and recall.
"""
