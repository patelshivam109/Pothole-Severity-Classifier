# Dataset Limitations & Future Work

## 1. Current Project Limitations
1. **Dataset Nature**: The dataset is image/object-annotation based.
2. **Feature Origin**: All features are derived strictly from bounding boxes in image space, not real-world dimensions.
3. **Severity Definition**: Severity labels are manually annotated subjective categories.
4. **No Physical Measurements**: No real-world physical pothole measurements exist (e.g., depth, physical volume).
5. **No Road Condition**: No road-condition baseline variables exist.
6. **No Traffic Data**: No traffic exposure or volume metrics are available.
7. **No Geographic Tracking**: No GPS coordinates or road segment IDs exist.
8. **No Maintenance History**: No historical repair records are documented.
9. **No Cost Data**: No labor, material, or historical repair cost data exists. Thus, actual financial cost prediction is impossible.
10. **Priority Status**: The priority score is a project-defined decision-support framework derived from model probabilities, not a scientifically validated or municipal standard.

## 2. Future Work & Data Collection Recommendations
Rather than fabricating values, we strongly recommend expanding data collection integrations:
- **GPS Integration**: Tag images with precise geospatial coordinates to cluster repairs geographically.
- **Cost Data Integration**: Maintain a database of repair dimensions and corresponding financial cost to model labor/materials.
- **Traffic Modeling**: Intersect the geographic data with municipal AADT (Annual Average Daily Traffic) maps to prioritize based on user exposure.
- **Physical Sensing**: Use depth-sensing (e.g., LiDAR) to capture the Z-axis physical volume for a vastly superior structural severity assessment.
