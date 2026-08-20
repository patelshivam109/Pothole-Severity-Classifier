import pandas as pd
import os

def assign_priority_category(row):
    # Review Required if confidence is extremely low
    if row['prediction_confidence'] < 0.45:
        return 'REVIEW REQUIRED', True
    
    # Priority Score = 3 * p(major) + 2 * p(medium) + 1 * p(minor)
    score = row['priority_score']
    
    # 4-tier decision support thresholds
    if score >= 2.6:
        return 'CRITICAL', False
    elif score >= 2.0:
        return 'HIGH', False
    elif score >= 1.4:
        return 'MEDIUM', False
    else:
        return 'LOW', False

def run_priority_analysis():
    # Load final predictions
    df_all = pd.read_csv('outputs/predictions/final_pothole_analysis.csv')
    
    # Re-apply updated 4-tier categories
    df_all[['priority_category', 'review_required']] = df_all.apply(
        lambda row: pd.Series(assign_priority_category(row)), axis=1
    )
    
    # Save the updated priority
    df_all.to_csv('outputs/prioritization/updated_pothole_priority.csv', index=False)
    
    # Image-level inspection prioritization
    image_summary = df_all.groupby('filename').agg(
        pothole_count=('predicted_severity', 'count'),
        minor_count=('predicted_severity', lambda x: (x == 'minor_pothole').sum()),
        medium_count=('predicted_severity', lambda x: (x == 'medium_pothole').sum()),
        major_count=('predicted_severity', lambda x: (x == 'major_pothole').sum()),
        highest_predicted_severity=('predicted_severity', lambda x: 'major_pothole' if 'major_pothole' in x.values else ('medium_pothole' if 'medium_pothole' in x.values else 'minor_pothole')),
        priority_score_max=('priority_score', 'max'),
        confidence_min=('prediction_confidence', 'min'),
        review_flag=('review_required', 'any')
    ).reset_index()
    
    # Apply category logic to the image-level max score
    image_summary['priority_category'] = image_summary.apply(
        lambda row: 'REVIEW REQUIRED' if row['review_flag'] else (
            'CRITICAL' if row['priority_score_max'] >= 2.6 else (
            'HIGH' if row['priority_score_max'] >= 2.0 else (
            'MEDIUM' if row['priority_score_max'] >= 1.4 else 'LOW'
        ))), axis=1
    )
    
    image_summary.to_csv('outputs/prioritization/image_priority_ranking.csv', index=False)
    return df_all, image_summary

if __name__ == '__main__':
    run_priority_analysis()
    print("Priority analysis completed.")
