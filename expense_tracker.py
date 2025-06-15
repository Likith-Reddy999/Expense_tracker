import os
import csv
from datetime import datetime

filename = "expense.csv"

def initialize():
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Amount", "Category", "Date"])

def add_expense(amount, category, date):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([amount, category, date])

initialize()

while True:
    print("\n --- Expense Tracker ---")
    print("1. Add Expense")
    print("2. View all Expenses")
    print("3. View Total Spent")
    print("4. Filter by Category")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ").strip()

    if choice == '1':
        amount = float(input("Enter amount: "))
        category = input("Enter category: ").strip()
        date = input("Enter date (YYYY-MM-DD): ").strip()
        datetime.strptime(date, "%Y-%m-%d")
        add_expense(amount, category, date)
        print("Expense added!")

    elif choice == '2':
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            print("\nYour Expenses:")
            for row in reader:
                print(f"Amount: ${row[0]}, Category: {row[1]}, Date: {row[2]}")

    elif choice == '3':
        total = 0.0
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                total += float(row[0])
        print(f"\nTotal spent: ${total:.2f}")

    elif choice == '4':
        filtering = input("Enter category to filter: ").strip().lower()
        found = False
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            print(f"\nExpenses in '{filtering}' category:")
            for row in reader:
                if row[1].strip().lower() == filtering:
                    print(f"Amount: ${row[0]}, Date: {row[2]}")
                    found = True
        if not found:
            print("No expenses found in this category.")

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid option! Please choose 1 to add data or 2 to exit.")
