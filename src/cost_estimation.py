import pandas as pd

def calculate_costs(df, base_cost):
    """
    Cost = Base_Cost * Severity_Multiplier * (1 + Size_Factor)
    
    Where:
    - Severity Multiplier: major=3.0, medium=1.5, minor=1.0
    - Size Factor: rel_bbox_area (relative size of pothole in image space, mostly 0 to 0.5)
    """
    severity_multipliers = {
        'major_pothole': 3.0,
        'medium_pothole': 1.5,
        'minor_pothole': 1.0
    }
    
    costs = []
    for _, row in df.iterrows():
        sev = row['predicted_severity']
        mult = severity_multipliers.get(sev, 1.0)
        size_factor = row['rel_bbox_area']
        
        # Transparent expected cost formula
        cost = base_cost * mult * (1.0 + size_factor)
        costs.append(cost)
        
    return costs

def run_cost_estimation():
    df = pd.read_csv('outputs/prioritization/updated_pothole_priority.csv')
    
    # 3 Scenarios
    scenarios = {
        'Low Cost': 50,
        'Baseline Cost': 100,
        'High Cost': 200
    }
    
    summary = []
    
    for scenario_name, base in scenarios.items():
        df[f'{scenario_name}_Estimate'] = calculate_costs(df, base)
        
        total = df[f'{scenario_name}_Estimate'].sum()
        by_severity = df.groupby('predicted_severity')[f'{scenario_name}_Estimate'].sum().to_dict()
        by_priority = df.groupby('priority_category')[f'{scenario_name}_Estimate'].sum().to_dict()
        
        summary.append({
            'Scenario': scenario_name,
            'Base Cost Assumption': base,
            'Total Estimated Planning Cost': total,
            'Major Pothole Cost': by_severity.get('major_pothole', 0),
            'Medium Pothole Cost': by_severity.get('medium_pothole', 0),
            'Minor Pothole Cost': by_severity.get('minor_pothole', 0),
            'Critical Priority Cost': by_priority.get('CRITICAL', 0),
            'High Priority Cost': by_priority.get('HIGH', 0),
            'Medium Priority Cost': by_priority.get('MEDIUM', 0),
            'Low Priority Cost': by_priority.get('LOW', 0),
            'Review Required Cost': by_priority.get('REVIEW REQUIRED', 0)
        })
        
    df.to_csv('outputs/cost_estimation/scenario_cost_estimates.csv', index=False)
    
    df_summary = pd.DataFrame(summary)
    df_summary.to_csv('outputs/cost_estimation/cost_scenario_summary.csv', index=False)
    return df, df_summary

if __name__ == '__main__':
    run_cost_estimation()
    print("Cost estimation completed.")
