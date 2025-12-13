# Deep Dive: Scikit-Learn (`sklearn`)

The industry standard for "Classical" Machine Learning (Regression, SVM, Random Forest, K-Means).

---

## 1. The Estimator API

Uniform interface for everything.
*   `fit(X, y)`: Learn from data.
*   `predict(X)`: Predict new data.
*   `transform(X)`: Modify data (preprocessing).

---

## 2. Pipelines (`make_pipeline`)

Chaining Preprocessing and Modeling into a single object. Prevents DATA LEAKAGE (fitting scalers on test data).

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# 1. Scale data (Mean=0, Var=1)
# 2. Apply SVM
clf = make_pipeline(StandardScaler(), SVC())

clf.fit(X_train, y_train) # Calls fit on Scaler, transforms X, fits SVC
clf.predict(X_test)       # Calls transform on Scaler, predicts with SVC
```

---

## 3. Cross-Validation

Never rely on a single train/test split. `cross_val_score` trains K variations.

```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(clf, X, y, cv=5)
print(f"Accuracy: {scores.mean()} (+/- {scores.std()})")
```
