<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange.svg" alt="ML">
  <img src="https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/Data%20Viz-Plotly-indigo.svg" alt="Plotly">
  <img src="https://img.shields.io/badge/Status-Completed-success.svg" alt="Status">

  <h1>🛣️ Pothole Severity Classifier & Maintenance Decision Support System</h1>
  <p>An end-to-end AI/ML workflow for municipal road infrastructure triage, repair prioritization, and scenario-based cost planning.</p>
</div>

---

## 📖 Project Overview
Municipalities face severe resource constraints when identifying and repairing road infrastructure damage. Without automated triage, minor distresses escalate into major structural failures. 

This project leverages machine learning to automatically classify pothole severity from spatial inspection data, rank repair priorities, and output scheduling recommendations to optimize maintenance budgets.

## ✨ Key Features
* **Severity Classification**: AI models trained to predict damage tiers (Minor, Medium, Major) directly from bounding box geometry.
* **Leak-Safe Engineering**: Robust `GroupKFold` cross-validation ensuring images from the same geographic source do not bleed across training splits.
* **Priority Framework**: A continuous, 4-tier decision-support engine (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) derived mathematically from class prediction probabilities.
* **Cost Estimation Engine**: A transparent, scenario-based financial planning tool supporting USD ($) and INR (₹) that avoids hallucinating historical receipts.
* **Interactive Dashboard**: A premium, glassmorphism-styled Streamlit UI featuring Plotly analytics, hotspot identification, and interactive budget sliders.

## 🛠️ Technology Stack
* **Core:** Python, Pandas, NumPy
* **Machine Learning:** Scikit-Learn, Support Vector Machine (RBF Kernel), Gradient Boosting, XGBoost
* **Data Visualization:** Plotly, Seaborn, Matplotlib
* **Web Deployment:** Streamlit.

## 📂 Project Architecture
```text
Pothole-Severity-Classifier/
├── Dataset/                   # Pascal VOC image dataset (Raw & Processed)
├── Documentation/             # Official Internship Final Report (.docx)
├── dashboard/
│   └── app.py                 # Premium Streamlit UI Application
├── models/                    # Exported .joblib models (Final SVM)
├── notebooks/
│   ├── 01_data_preprocessing_and_eda.ipynb
│   ├── 02_feature_engineering_and_data_splitting.ipynb
│   ├── 03_model_training_and_comparison.ipynb
│   ├── 04_model_optimization_prediction_and_priority.ipynb
│   └── 05_final_analysis_and_reporting.ipynb
├── outputs/                   # Final predicted CSV datasets & cost metrics
├── reports/                   # Technical Markdown Reports & Requirement Audits
├── src/                       # Production Python Modules (Priorities, Costs)
├── requirements.txt           # Project dependencies
└── README.md
```

## 📊 Model Performance
Five distinct classification models were evaluated. The **Support Vector Machine (SVM)** was selected for the final deployment due to its superior generalization against spatial coordinate overfitting.

| Model | Macro F1 Score | Accuracy |
|-------|----------------|----------|
| **Support Vector Machine** | **65.14%** | **65.43%** |
| Gradient Boosting | 59.74% | 58.26% |
| LightGBM | 58.42% | 56.66% |
| Random Forest | 58.09% | 56.20% |
| XGBoost | 57.10% | 54.71% |

## 🚀 How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/patelshivam109/Pothole-Severity-Classifier.git
   cd Pothole-Severity-Classifier
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Dashboard:**
   ```bash
   python -m streamlit run dashboard/app.py
   ```
   *The dashboard will automatically open in your default browser at `http://localhost:8501`.*

## ⚠️ Dataset Limitations & Academic Integrity
To maintain rigorous academic and professional integrity, this project explicitly notes the limitations of the provided dataset:
- **No GPS Data:** Geographic road segment mapping is unavailable. Image files are used as proxy "hotspots".
- **No Traffic/Condition Data:** AADT, IRI, and PCI condition indices are unavailable.
- **No Historical Receipts:** Supervised cost regression is impossible. The project utilizes a configurable heuristic scenario-based cost framework instead.

## 🤝 Acknowledgements
Project submitted by **Shivam Subedar Patel** (Intern AI/ML) for **Data Vidwan**.
