import sqlite3

conn = sqlite3.connect("expenses.db")  # creates file if it doesn't exist
cursor = conn.cursor()

def initialize():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()

def add_expense(amount,category,date):
    cursor.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ? ,?)",(amount,category,date))
    conn.commit()

def view_expenses():
    cursor.execute("SELECT amount, category, date FROM expenses")
    rows = cursor.fetchall()
    print("\nYOur Expenses:")
    for row in rows:
        print(f"Amount: ${row[0]},category:{row[1]},Date:{row[2]}")

def total_spent():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]
    print(f"\nTotal spent: ${total:.2f}" if total else "No expenses yet.")

def filter_by_category(category):
    cursor.execute("SELECT amount, date FROM expenses WHERE LOWER(category) = ?", (category.lower(),))
    rows = cursor.fetchall()
    if not rows:
        print("No expenses found in this category.")
    else:
        print(f"\nExpenses in '{category}' category:")
        for row in rows:
            print(f"Amount: ${row[0]}, Date: {row[1]}")

initialize()

while True:
    print("\n--- Expense Tracker ---")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. View Total Spent")
    print("4. Filter by Category")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ").strip()

    if choice == '1':
        amount = float(input("Enter amount: "))
        category = input("Enter category: ").strip()
        date = input("Enter date (YYYY-MM-DD): ").strip()
        add_expense(amount, category, date)
        print("Expense added!")

    elif choice == '2':
        view_expenses()

    elif choice == '3':
        total_spent()

    elif choice == '4':
        category = input("Enter category to filter: ").strip()
        filter_by_category(category)

    elif choice == '5':
        print("Goodbye!")
        break

    else:
        print("Invalid option. Please choose between 1 and 5.")
