# Simplified ETL Pipeline

import csv
import sqlite3
import json

def extract_data(file_path):
    """Extract data from CSV file."""
    data = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['quantity'] = int(row['quantity'])
            row['price'] = float(row['price'])
            data.append(row)
    return data

def transform_data(data):
    """Transform data: calculate total for each item."""
    for item in data:
        item['total'] = item['quantity'] * item['price']
    return data

def load_data(data, db_path):
    """Load data into SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            quantity INTEGER,
            price REAL,
            total REAL
        )
    ''')
    for item in data:
        cursor.execute('''
            INSERT INTO sales (quantity, price, total)
            VALUES (?, ?, ?)
        ''', (item['quantity'], item['price'], item['total']))
    conn.commit()
    conn.close()

def generate_report(db_path, output_file):
    """Generate a simple sales report."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(total), COUNT(*) FROM sales')
    total_sales, count = cursor.fetchone()
    report = {
        'total_sales': total_sales,
        'number_of_sales': count
    }
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=4)
    conn.close()

if __name__ == "__main__":
    # Extract
    data = extract_data('sales_data.csv')

    # Transform
    transformed_data = transform_data(data)

    # Load
    load_data(transformed_data, 'sales.db')

    # Generate report
    generate_report('sales.db', 'sales_report.json')

    print("ETL Pipeline completed")