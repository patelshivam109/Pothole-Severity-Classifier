# Municipal Repair Planning Report

## 1. Project Objective
The objective of this project is to provide a comprehensive decision-support system for municipal road infrastructure maintenance, leveraging computer vision techniques to classify pothole severity and prioritize repair efforts.

## 2. Dataset
- **717** Source Images
- **1,886** Cleaned Pothole Annotations
- Image-derived bounding boxes

## 3. Final Model
The selected model is a hyperparameter-tuned **Support Vector Machine (SVM)** with an RBF kernel. It demonstrated the strongest performance and most reliable probability distribution across cross-validation folds.

## 4. Severity Classification Results (Held-Out Test Set)
- **Accuracy**: 65.43%
- **Macro F1**: 65.14%

**Per-Class Test F1:**
- Major Pothole: 73%
- Medium Pothole: 63%
- Minor Pothole: 59%

## 5. Priority Methodology
We implemented a continuous Expected Severity Priority Score derived from the final SVM's output probabilities:
`Score = (3 * probability_major) + (2 * probability_medium) + (1 * probability_minor)`

## 6. Priority Distribution
The 1,886 predicted potholes were mapped into the following official project decision-support categories:
- **CRITICAL**: Score >= 2.6
- **HIGH**: 2.0 <= Score < 2.6
- **MEDIUM**: 1.4 <= Score < 2.0
- **LOW**: Score < 1.4
- **REVIEW REQUIRED**: Maximum predicted confidence < 0.45

## 7. Image-Level Inspection Prioritization
Because the dataset lacks true road segment IDs and GPS coordinates, we performed prioritization at the *inspection image* level. Images containing multiple major potholes are flagged with the highest aggregated priority score, allowing maintenance crews to target high-density hotspots.

## 8. Maintenance Scheduling Recommendations
- **CRITICAL**: Immediate inspection / highest maintenance planning priority
- **HIGH**: Near-term inspection and planned maintenance
- **MEDIUM**: Scheduled maintenance queue
- **LOW**: Routine monitoring
- **REVIEW REQUIRED**: Manual inspection before normal scheduling

## 9. Scenario-Based Cost Planning
To assist with budgeting, a transparent scenario-based cost module was deployed. It applies configurable severity multipliers and bounding-box size factors to assumed base costs (Low, Baseline, High), rather than attempting to predict historical costs from absent data.

## 10. Limitations
The supplied dataset strictly limits the scope of this project. It does not contain GPS, traffic volume, road condition measurements, or historical maintenance costs. Consequently, geographic road mapping, genuine road-segment ranking, and supervised historical cost prediction are unavailable.

## 11. Recommended Future Data Collection
We highly recommend augmenting the image capture process with:
1. Automatic GPS tagging.
2. Depth-sensing LiDAR for true volumetric severity.
3. Database integration to map inspection imagery to actual maintenance tickets and final repair costs.
