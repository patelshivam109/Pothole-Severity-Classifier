# Maintenance Cost Estimation Report

## 1. Objective
The objective of this module is to estimate the financial cost of repairing the classified potholes to assist municipal planning and budgeting.

## 2. Available Data
The underlying dataset is a Pascal VOC image/object-detection dataset. It contains pothole bounding boxes (in pixel-space) and manually annotated severity categories.

## 3. Missing Cost Information
The dataset lacks:
- **Historical observed repair costs**
- **Labor rates**
- **Material volumes**
- **Real-world spatial dimensions (depth/area)**

## 4. Why Supervised Cost Prediction is Not Possible
A genuine supervised machine learning cost regression model requires a target variable (actual historical cost) mapped to physical predictor variables. Because no such target or physical variables exist, training an ML model to predict "actual" cost would be mathematically baseless and dangerously misleading. 

## 5. Scenario-Based Methodology
Instead of fabricating a fake predictive model, we implemented a **Transparent Scenario-Based Cost Estimation Framework**. This decision-support tool allows users to apply sensible, configurable assumptions to the model's outputs to plan budgets conditionally.

## 6. Formula
`Estimated Cost = Base_Cost_Assumption * Severity_Multiplier * (1 + Size_Factor)`

Where `Size_Factor` is the relative bounding box area of the pothole in the image.

## 7. Configurable Assumptions
- **Base Cost**: Can be set to any dollar amount depending on the municipal budget scenario.
- **Severity Multipliers**: 
  - Major Pothole = 3.0x
  - Medium Pothole = 1.5x
  - Minor Pothole = 1.0x

## 8. Low/Baseline/High Scenarios
We generated three static scenarios for the dashboard:
- **Low Cost Scenario**: Base Cost = $50
- **Baseline Cost Scenario**: Base Cost = $100
- **High Cost Scenario**: Base Cost = $200

## 9. Aggregate Planning Estimates
These scenarios are aggregated by Priority and Severity to provide immediate budget requirement estimations across the entire prioritized queue.

## 10. Limitations
These estimates are strictly hypothetical planning figures derived from image-space bounding boxes and assumed unit costs. They must **not** be interpreted as historical costs or precise repair quotes.

## 11. Future Requirements for a True Cost Model
To transition this module from scenario-planning to predictive forecasting, the municipality must integrate a historical maintenance database linking repair tickets (labor hours + material volume = actual cost) to the specific pothole imagery.
