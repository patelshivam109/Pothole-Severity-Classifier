import pandas as pd
import json

def load_data():
    df = pd.read_csv('outputs/scheduling/maintenance_schedule_recommendations.csv')
    image_df = pd.read_csv('outputs/prioritization/image_priority_ranking.csv')
    cost_summary = pd.read_csv('outputs/cost_estimation/cost_scenario_summary.csv')
    return df, image_df, cost_summary

def load_metrics():
    with open('models/final/final_model_metadata.json', 'r') as f:
        meta = json.load(f)
    return meta
