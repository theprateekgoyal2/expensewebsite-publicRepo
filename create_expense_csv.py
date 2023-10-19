import csv
import datetime
import random

# Sample categories
categories = ["Food", "Travel", "Rent", "Entertainment"]

# Generate 50 items of sample data
data = []
for _ in range(100):
    year = 2023
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    random_date = datetime.date(year, month, day).strftime('%Y-%m-%d')
    item = {
        "amount": round(random.uniform(5, 100), 2),  # Random amount between 5 and 100
        "category": random.choice(categories),  # Random category
        "date": str(random_date),
        "description": f"Expense-{_ + 1}",
    }
    print(item)
    data.append(item)

# Define the CSV file name
csv_file = "expenses_data.csv"

# Write data to the CSV file
with open(csv_file, "w", newline="") as csvfile:
    fieldnames = ["amount", "category", "date", "description"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    # writer.writeheader()

    # Write the data
    for row in data:
        writer.writerow(row)

print(f"Data for 100 items has been written to {csv_file}.")
