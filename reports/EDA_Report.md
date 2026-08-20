# EDA Report

## 1. Dataset Overview
- The dataset consists of XML annotations mapping to images.
- Extracted structured data has 1886 rows and 14 columns.

## 2. Target Variable
- Target variable is `class`.
- Classes: medium_pothole, minor_pothole, major_pothole
- There is a noticeable imbalance.

## 3. Missing Variables (Limitations)
- No road condition variables.
- No location/segment information.
- No traffic exposure or environmental variables.
- No maintenance cost fields.

## 4. Key Findings
- **Pothole Dimensions**: Major potholes generally exhibit larger bounding box areas, widths, and heights compared to minor and medium potholes.
- **Correlations**: Width, height, and area are strongly positively correlated, as expected.
- **Severity Patterns**: The physical size of the pothole in the image strongly relates to its annotated severity.

