import os
import json
import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas 

expenses = []

def load_data():
    global expenses
    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)
    except:
        expenses = []

def save_data():
    with open("expenses.json", "w") as file:
        json.dump("expenses, file")

def generate_pdf():
    if not os.path.exists("expenses"):
        os.makedirs("expenses")

    file_path = "expenses/{expense}.pdf"
    c = canvas.Canvas(file_path, pagesize = letter)

    y = 750
    c.setFont("Helvetica-bold", 14)
    c.drawString(200, 800, f"Expenses List")
    y -= 30

    for e in expenses:
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = 750

        c.setFont("Helvetica", 10)
        line = f"{e["Amount"]} | {e["Date"]} | {e["Description"]} | {e["Category"]}"
        c.drawString(50, y, line)
        y -= 20

        c.save()
        messagebox.showinfo(f"PDF exported!")

def add_expense():
    amount = int(amount_entry.get())
    date = date_entry.get()
    description = desc_entry.get()
    category = cate_entry.get()

    if description == "" or category == "":
        messagebox.showerror(f"Error", "Description and category required!")
        return
    
    expense = {
        "Amount": amount,
        "Date": date,
        "Description": description,
        "Category": category
    }

    expenses.append(expense)
    save_data()
    messagebox.showinfo("Added", "Expense added!")

    clear_fields()

def show_all():
    if not expenses:
        messagebox.showerror(f"Error", "No expense found!")
        return
    
    for e in expenses:
        resultbox.insert(tk.END, f"{e['Amount']} | {e['Date']} | {e['Description']} | {e['Category']}")
        
def search_expense():
    if not expenses:
        messagebox.showerror(f"Error", "No expense found!")
        return
    
    description = desc_entry.get()
    category = cate_entry.get()

    for e in expenses:
        if e["Description"] == description or e["Category"] == category:
            resultbox.insert(tk.END, f"{e['Amount']} | {e['Date']} | {e['Description']} | {e['Category']}")
            messagebox.showinfo("Success", "Expense found!")
            return
    
    clear_fields()
        
def delete_expense():
    description = desc_entry.get()
    category = cate_entry.get()

    for e in expenses:
        if e["Description"] == description or e["Category"] == category:
            expenses.remove(e)
            save_data()
            messagebox.showinfo("Deleted", "Expense deleted!")
            return
        
    messagebox.showerror(f"Error", "No expense found!")

def total_expense():
    total = 0
    for e in expenses:
        total += e["Amount"]
        messagebox.showinfo(f"Total", "Total expense found!")
        resultbox.insert(tk.END, f"Total: {total}")

def clear_fields():
    amount_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    cate_entry.delete(0, tk.END)

# ..... GUI .....
bg ="#2C2F33"
fg = "#FFFFFF"

root = tk.Tk()
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.configure(bg="black")
btn_color = "#112C91"

root.title("EXPENSE TRACKER")
tk.Label(root, text = "EXPENSE TRACKER", bg="#2c2c3e", fg="white", font = ("Arial", 20, "bold")).grid(row = 0, column = 0, columnspan = 2, pady = 5)
root.geometry("500x700")

# INPUTS
input_frame = tk.Frame(root, bg = "#2c2c3e")
input_frame.grid(row=1, column=0, padx=20, pady=20)

tk.Label(input_frame, text = "Amount", bg="#2c2c3e", fg="white", font=("Arial", 10, "bold")).grid(row = 0, column = 0, padx =5, pady = 5)
amount_entry = tk.Entry(input_frame, bg="#3a3a4f", fg="white", insertbackground="white")
amount_entry.grid(row = 0, column = 1, padx =5, pady = 5)

tk.Label(input_frame, text = "Date", bg="#2c2c3e", fg="white", font=("Arial", 10, "bold")).grid(row = 0, column = 2, padx =5, pady = 5)
date_entry = tk.Entry(input_frame, bg="#3a3a4f", fg="white", insertbackground="white")
date_entry.grid(row = 0, column = 3, padx =5, pady = 5)

tk.Label(input_frame, text = "Description", bg="#2c2c3e", fg="white", font=("Arial", 10, "bold")).grid(row = 1, column = 0, padx =5, pady = 5)
desc_entry = tk.Entry(input_frame, bg="#3a3a4f", fg="white", insertbackground="white")
desc_entry.grid(row = 1, column = 1, padx =5, pady = 5)

tk.Label(input_frame, text = "Category", bg="#2c2c3e", fg="white", font=("Arial", 10, "bold")).grid(row = 1, column = 2, padx =5, pady = 5)
cate_entry = tk.Entry(input_frame, bg="#3a3a4f", fg="white", insertbackground="white")
cate_entry.grid(row = 1, column = 3, padx =5, pady = 5)

tk.Label(input_frame, text = "Search", bg="#2c2c3e", fg="white", font=("Arial", 10, "bold")).grid(row = 2, column = 0, padx =5, pady = 5)
cate_entry = tk.Entry(input_frame, bg="#3a3a4f", fg="white", insertbackground="white")
cate_entry.grid(row = 2, column = 1, padx =5, pady = 5)

# BUTTONS
button_frame = tk.Frame(root, bg="#2c2c3e")
button_frame.grid(row=2, column=0, padx=20, pady=15)

btn_add = tk.Button(button_frame, text = "Add Expense", width=15, command = add_expense, bg="brown", fg="white", activebackground="#357abd")
btn_add.grid(row=0, column=0, padx=5, pady=5)

btn_all = tk.Button(button_frame, text = "Show All", width=15, command = show_all, bg="brown", fg="white", activebackground="#357abd")
btn_all.grid(row=0, column=1, padx=5, pady=5)

btn_search = tk.Button(button_frame, text = "Search Expense", width=15, command = search_expense, bg="brown", fg="white", activebackground="#357abd")
btn_search.grid(row=0, column=2, padx=5, pady=5)

btn_delete = tk.Button(button_frame, text = "Delete Expense", width=15, command = delete_expense, bg="brown", fg="white", activebackground="#357abd")
btn_delete.grid(row=1, column=0, padx=5, pady=5)

btn_total = tk.Button(button_frame, text = "Total Expense", width=15, command = total_expense, bg="brown", fg="white", activebackground="#357abd")
btn_total.grid(row=1, column=1, padx=5, pady=5)

btn_exp = tk.Button(button_frame, text = "Export PDF", width=15, bg="brown", fg="white", activebackground="#357abd")
btn_exp.grid(row=1, column=2, padx=5, pady=5)

# OUTPUT
resultbox = tk.Listbox(root, width = 50, height = 15)
resultbox.grid(row = 3, column = 0, rowspan = 8, pady = 20)

load_data()
root.mainloop()











