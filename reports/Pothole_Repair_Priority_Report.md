# Pothole Repair Priority Report

## 1. Decision-Support Framework
The model outputs probability values for each severity class. These are transformed into an **Expected Severity Priority Score**:
`Score = (3 * probability_major) + (2 * probability_medium) + (1 * probability_minor)`

This score scales linearly from 1.0 (certain minor) to 3.0 (certain major). It balances model certainty and structural severity safely.

## 2. Priority Thresholds & Recommendations
- **HIGH PRIORITY** (Score >= 2.5): Prioritize inspection/maintenance review. (Count: 468)
- **MEDIUM PRIORITY** (1.5 <= Score < 2.5): Schedule inspection and maintenance planning. (Count: 1245)
- **LOW PRIORITY** (Score < 1.5): Monitor and include in routine maintenance review. (Count: 168)
- **REVIEW REQUIRED** (Max Probability < 0.45): Manual inspection recommended because model confidence is low and ambiguous. (Count: 5)

## 3. Image-Level Aggregation
We successfully aggregated pothole classifications at the source image level to identify hotspots within the dataset bounds.
