# Advanced Python data processing script without external libraries

import csv
import json
from collections import defaultdict
from datetime import datetime

def load_csv(file_path):
    """Load CSV data into a list of dictionaries."""
    data = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert values to appropriate types
            row['value'] = float(row['value'])
            row['date'] = datetime.strptime(row['date'], '%Y-%m-%d')
            data.append(row)
    return data

def validate_data(data):
    """Validate data: check for missing values, invalid dates."""
    valid_data = []
    for row in data:
        if all(k in row and row[k] is not None for k in ['id', 'value', 'date']):
            if row['value'] >= 0:
                valid_data.append(row)
    return valid_data

def aggregate_by_month(data):
    """Aggregate data by month: sum values."""
    monthly = defaultdict(float)
    for row in data:
        month_key = row['date'].strftime('%Y-%m')
        monthly[month_key] += row['value']
    return dict(monthly)

def save_json(data, file_path):
    """Save data to JSON."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4, default=str)

if __name__ == "__main__":
    # Load and process data
    raw_data = load_csv('sample_data.csv')
    valid_data = validate_data(raw_data)
    aggregated = aggregate_by_month(valid_data)
    save_json(aggregated, 'monthly_summary.json')
    print("Processing completed. Check monthly_summary.json")