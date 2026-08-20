import pandas as pd

def assign_schedule(row):
    cat = row['priority_category']
    if cat == 'CRITICAL':
        return 'Immediate inspection / highest maintenance planning priority', 'Immediate Review'
    elif cat == 'HIGH':
        return 'Near-term inspection and planned maintenance', 'Near-Term Planning'
    elif cat == 'MEDIUM':
        return 'Scheduled maintenance queue', 'Scheduled Maintenance'
    elif cat == 'LOW':
        return 'Routine monitoring', 'Routine Monitoring'
    elif cat == 'REVIEW REQUIRED':
        return 'Manual inspection before normal scheduling', 'Immediate Review'
    else:
        return 'Unknown', 'Unknown'

def run_scheduler():
    df = pd.read_csv('outputs/cost_estimation/scenario_cost_estimates.csv')
    
    df[['recommended_action', 'recommended_planning_window']] = df.apply(
        lambda row: pd.Series(assign_schedule(row)), axis=1
    )
    
    # Save the full data with recommendations
    df.to_csv('outputs/scheduling/maintenance_schedule_recommendations.csv', index=False)
    return df

if __name__ == '__main__':
    run_scheduler()
    print("Scheduling completed.")
