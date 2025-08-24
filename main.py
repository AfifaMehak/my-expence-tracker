import sqlite3
import csv
import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

# =========================
# DATABASE FUNCTIONS
# =========================
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        notes TEXT
    )
    ''')
    conn.commit()
    conn.close()

def add_expense(amount, category, date, notes):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('INSERT INTO expenses (amount, category, date, notes) VALUES (?, ?, ?, ?)',
              (amount, category, date, notes))
    conn.commit()
    conn.close()

def view_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses')
    rows = c.fetchall()
    conn.close()
    return rows

def delete_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()

def search_expenses(keyword):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses WHERE category LIKE ? OR date LIKE ?", 
              (f'%{keyword}%', f'%{keyword}%'))
    rows = c.fetchall()
    conn.close()
    return rows

def export_to_csv():
    today = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"expenses_{today}.csv"
    rows = view_expenses()
    if rows:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Amount", "Category", "Date", "Notes"])
            writer.writerows(rows)
        messagebox.showinfo("Export Successful", f"Data exported to {filename}")
    else:
        messagebox.showerror("Error", "No expenses to export!")

# =========================
# GUI FUNCTIONS
# =========================
def add_expense_gui():
    amount = entry_amount.get()
    category = entry_category.get()
    date = entry_date.get()
    notes = entry_notes.get()

    if amount and category and date:
        try:
            add_expense(float(amount), category, date, notes)
            messagebox.showinfo("Success", "Expense added!")
            entry_amount.delete(0, END)
            entry_category.delete(0, END)
            entry_date.delete(0, END)
            entry_notes.delete(0, END)
            view_expenses_gui()
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
    else:
        messagebox.showerror("Error", "Please fill in all required fields.")

def view_expenses_gui():
    rows = view_expenses()
    text_output.delete("1.0", END)
    if rows:
        for row in rows:
            text_output.insert(END, f"ID: {row[0]} | Amount: {row[1]} | Category: {row[2]} | Date: {row[3]} | Notes: {row[4]}\n")
    else:
        text_output.insert(END, "No expenses found.\n")

def delete_expense_gui():
    expense_id = entry_delete_id.get()
    if expense_id:
        try:
            delete_expense(int(expense_id))
            messagebox.showinfo("Success", f"Expense ID {expense_id} deleted!")
            entry_delete_id.delete(0, END)
            view_expenses_gui()
        except ValueError:
            messagebox.showerror("Error", "Expense ID must be a number.")
    else:
        messagebox.showerror("Error", "Please enter an Expense ID.")

def search_expenses_gui():
    keyword = entry_search.get()
    if keyword:
        rows = search_expenses(keyword)
        text_output.delete("1.0", END)
        if rows:
            for row in rows:
                text_output.insert(END, f"ID: {row[0]} | Amount: {row[1]} | Category: {row[2]} | Date: {row[3]} | Notes: {row[4]}\n")
        else:
            text_output.insert(END, "No matching expenses found.\n")
    else:
        messagebox.showerror("Error", "Please enter a search keyword.")

# =========================
# MAIN PROGRAM
# =========================
init_db()

app = ttk.Window(themename="superhero")  # Dark modern theme
app.title("💰 Expense Tracker")
app.geometry("600x600")

# Title
ttk.Label(app, text="Expense Tracker", font=("Helvetica", 18, "bold")).pack(pady=10)

# Input Frame
frame_inputs = ttk.Frame(app)
frame_inputs.pack(pady=5)

ttk.Label(frame_inputs, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
entry_amount = ttk.Entry(frame_inputs)
entry_amount.grid(row=0, column=1)

ttk.Label(frame_inputs, text="Category:").grid(row=1, column=0, padx=5, pady=5)
entry_category = ttk.Entry(frame_inputs)
entry_category.grid(row=1, column=1)

ttk.Label(frame_inputs, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
entry_date = ttk.Entry(frame_inputs)
entry_date.grid(row=2, column=1)

ttk.Label(frame_inputs, text="Notes:").grid(row=3, column=0, padx=5, pady=5)
entry_notes = ttk.Entry(frame_inputs)
entry_notes.grid(row=3, column=1)

# Buttons
ttk.Button(app, text="➕ Add Expense", bootstyle=SUCCESS, command=add_expense_gui).pack(pady=5)
ttk.Button(app, text="📋 View All Expenses", bootstyle=INFO, command=view_expenses_gui).pack(pady=5)

# Delete Section
frame_delete = ttk.Frame(app)
frame_delete.pack(pady=5)
ttk.Label(frame_delete, text="Delete by ID:").grid(row=0, column=0, padx=5)
entry_delete_id = ttk.Entry(frame_delete)
entry_delete_id.grid(row=0, column=1, padx=5)
ttk.Button(frame_delete, text="🗑 Delete Expense", bootstyle=DANGER, command=delete_expense_gui).grid(row=0, column=2, padx=5)

# Search Section
frame_search = ttk.Frame(app)
frame_search.pack(pady=5)
ttk.Label(frame_search, text="Search (Category/Date):").grid(row=0, column=0, padx=5)
entry_search = ttk.Entry(frame_search)
entry_search.grid(row=0, column=1, padx=5)
ttk.Button(frame_search, text="🔍 Search", bootstyle=WARNING, command=search_expenses_gui).grid(row=0, column=2, padx=5)

# Export Button
ttk.Button(app, text="💾 Export to CSV", bootstyle=PRIMARY, command=export_to_csv).pack(pady=5)

# Output Box
text_output = ttk.Text(app, height=12, width=70)
text_output.pack(pady=10)

app.mainloop()
