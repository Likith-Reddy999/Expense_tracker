import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# --- DB Setup ---
conn = sqlite3.connect("expenses.db")
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

def add_expense(amount, category, date):
    cursor.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
                   (amount, category, date))
    conn.commit()

def get_all_expenses():
    cursor.execute("SELECT amount, category, date FROM expenses")
    return cursor.fetchall()

def get_total_spent():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]
    return total if total else 0

def get_expenses_by_category(cat):
    cursor.execute("SELECT amount, date FROM expenses WHERE LOWER(category) = ?", (cat.lower(),))
    return cursor.fetchall()

# --- GUI Logic ---
def submit_expense(event=None):
    try:
        amount = float(amount_entry.get())
        category = category_entry.get().strip()
        date = date_entry.get().strip()
        datetime.strptime(date, "%d-%m-%Y")
        add_expense(amount, category, date)
        messagebox.showinfo("Success", "Expense added successfully!")
        amount_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        amount_entry.focus()
    except ValueError:
        messagebox.showerror("Error", "Please enter valid data. Date must be DD-MM-YYYY.")

def show_all_expenses():
    rows = get_all_expenses()
    if not rows:
        messagebox.showinfo("Expenses", "No expenses found.")
    else:
        result = "\n".join([f"₹{r[0]} | {r[1]} | {r[2]}" for r in rows])
        messagebox.showinfo("All Expenses", result)

def show_total_spent():
    total = get_total_spent()
    messagebox.showinfo("Total Spent", f"Total: ₹{total:.2f}")

def filter_by_category():
    cat = filter_entry.get().strip()
    if not cat:
        messagebox.showwarning("Input Missing", "Please enter a category.")
        return
    rows = get_expenses_by_category(cat)
    if not rows:
        messagebox.showinfo("No Results", f"No expenses found in '{cat}' category.")
    else:
        result = "\n".join([f"₹{r[0]} | {r[1]}" for r in rows])
        messagebox.showinfo(f"Expenses in '{cat}'", result)

# --- GUI Layout ---
initialize()
root = tk.Tk()
root.title("Expense Tracker")

# Labels and entries
tk.Label(root, text="Amount:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Date (DD-MM-YYYY):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
date_entry = tk.Entry(root)
date_entry.grid(row=2, column=1, padx=5, pady=5)

submit_btn = tk.Button(root, text="Add Expense", command=submit_expense)
submit_btn.grid(row=3, column=0, columnspan=2, pady=10)

# --- Extra Feature Buttons ---
tk.Button(root, text="View All", command=show_all_expenses).grid(row=4, column=0, pady=5)
tk.Button(root, text="Total Spent", command=show_total_spent).grid(row=4, column=1, pady=5)

# --- Filter ---
tk.Label(root, text="Filter by Category:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
filter_entry = tk.Entry(root)
filter_entry.grid(row=5, column=1, padx=5, pady=5)
tk.Button(root, text="Filter", command=filter_by_category).grid(row=6, column=0, columnspan=2, pady=5)

# Keyboard shortcuts
amount_entry.bind("<Return>", lambda e: category_entry.focus())
category_entry.bind("<Return>", lambda e: date_entry.focus())
date_entry.bind("<Return>", submit_expense)

amount_entry.focus()
root.mainloop()
