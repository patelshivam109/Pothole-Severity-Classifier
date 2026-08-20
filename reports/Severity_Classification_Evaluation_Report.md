# Severity Classification Evaluation Report

## 1. Dataset & Split
- Extracted features from bounding boxes using 1886 pothole instances.
- Split via GroupShuffleSplit using `filename` to strictly avoid image-level leakage across Train, Validation, and Test sets.

## 2. Baseline Models
Evaluated SVM, Gradient Boosting, XGBoost, LightGBM, and Random Forest.
- SVM Baseline F1: 0.6246
- Gradient Boosting Baseline F1: 0.5826

## 3. Hyperparameter Tuning & Selection
- Tuned SVM and Gradient Boosting using GroupKFold.
- SVM Tuned F1: 0.6555
- GB Tuned F1: 0.5965
- Selected Final Model: **Support Vector Machine**

## 4. Final Test Performance
Evaluated firmly on the untouched test set.
- Accuracy: 0.6543
- Macro F1: 0.6514
- ROC-AUC: 0.8325

## 5. Interpretability & Error Analysis
- The most important feature was `bbox_area` / geometry metrics.
- The bounding-box area is strongly associated with the model's severity predictions (image-space bounding-box area). We do NOT state that bbox_area physically causes severity.
- Errors predominantly occurred between ambiguous border classes (e.g. medium -> major or medium -> minor).

## 6. Limitations
The model predicts the manually annotated severity categories from image-derived object-detection features. The dataset does not contain:
- road condition
- traffic exposure
- environmental factors
- geographic road segment
- maintenance history
- repair cost
Therefore, the final classifier should be described strictly as a pothole severity classification model and NOT as a complete road-infrastructure deterioration prediction system.
