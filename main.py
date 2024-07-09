import tkinter as tk
from tkinter import messagebox, Menu
from tkinter import ttk
from dbOps import create_database, register_user, login_user, add_diary_entry, fetch_diary_entries, update_diary_entry, delete_diary_entry

# Function to register a user
def register():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    password = entry_password.get()

    if not first_name or not last_name or not email or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    if register_user(first_name, last_name, email, password):
        messagebox.showinfo("Success", "User registered successfully")
        entry_first_name.delete(0, tk.END)
        entry_last_name.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_password.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Email already registered")

# Function to login a user
def login():
    email = login_entry_email.get()
    password = login_entry_password.get()

    if not email or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    user = login_user(email, password)

    if user:
        messagebox.showinfo("Success", f"Welcome {user[1]}!")
    else:
        messagebox.showerror("Error", "Invalid email or password")

# Function to add a diary entry
def add_diary():
    title = diary_title_entry.get()
    content = diary_content_text.get("1.0", tk.END)

    if not title or not content.strip():
        messagebox.showerror("Error", "All fields are required")
        return

    add_diary_entry(title, content.strip(), 1)  # Replace 1 with the actual user_id after implementing login
    messagebox.showinfo("Success", "Diary entry added successfully")
    diary_title_entry.delete(0, tk.END)
    diary_content_text.delete("1.0", tk.END)
    display_diary_entries()

# Function to update a diary entry
def update_diary():
    selected_item = diary_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No diary entry selected")
        return

    entry_id = diary_tree.item(selected_item)['values'][0]
    title = diary_title_entry.get()
    content = diary_content_text.get("1.0", tk.END)

    if not title or not content.strip():
        messagebox.showerror("Error", "All fields are required")
        return

    update_diary_entry(entry_id, title, content.strip())
    messagebox.showinfo("Success", "Diary entry updated successfully")
    diary_title_entry.delete(0, tk.END)
    diary_content_text.delete("1.0", tk.END)
    display_diary_entries()

# Function to delete a diary entry
def delete_diary():
    selected_item = diary_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No diary entry selected")
        return

    entry_id = diary_tree.item(selected_item)['values'][0]
    delete_diary_entry(entry_id)
    messagebox.showinfo("Success", "Diary entry deleted successfully")
    display_diary_entries()

# Function to display diary entries
def display_diary_entries():
    for row in diary_tree.get_children():
        diary_tree.delete(row)

    entries = fetch_diary_entries(1)  # Replace 1 with the actual user_id after implementing login

    for entry in entries:
        diary_tree.insert("", tk.END, values=entry)

# Create the main application window
app = tk.Tk()
app.title("My Diary")

# Set styles
app.configure(bg="#333333")

# Create a menu bar
menu_bar = Menu(app, bg="#333333", fg="#FFFFFF")
app.config(menu=menu_bar)

# Create the Users menu
users_menu = Menu(menu_bar, tearoff=0, bg="#333333", fg="#FFFFFF")
menu_bar.add_cascade(label="Users", menu=users_menu)

# Create the Diary Records menu
diary_menu = Menu(menu_bar, tearoff=0, bg="#333333", fg="#FFFFFF")
menu_bar.add_cascade(label="Diary Records", menu=diary_menu)

# Create a Notebook (tabbed interface)
notebook = ttk.Notebook(app)
notebook.pack(pady=10, expand=True)

style = ttk.Style()
style.configure('TFrame', background='#333333')
# Create the Registration tab
registration_frame = ttk.Frame(notebook)

notebook.add(registration_frame, text="Register", padding=10)

# Create and place labels and entry widgets for the Registration form
tk.Label(registration_frame, text="First Name", bg="#333333", fg="#FFFFFF").grid(row=0, column=0, padx=10, pady=10)
entry_first_name = tk.Entry(registration_frame)
entry_first_name.grid(row=0, column=1, padx=10, pady=10)

tk.Label(registration_frame, text="Last Name", bg="#333333", fg="#FFFFFF").grid(row=1, column=0, padx=10, pady=10)
entry_last_name = tk.Entry(registration_frame)
entry_last_name.grid(row=1, column=1, padx=10, pady=10)

tk.Label(registration_frame, text="Email", bg="#333333", fg="#FFFFFF").grid(row=2, column=0, padx=10, pady=10)
entry_email = tk.Entry(registration_frame)
entry_email.grid(row=2, column=1, padx=10, pady=10)

tk.Label(registration_frame, text="Password", bg="#333333", fg="#FFFFFF").grid(row=3, column=0, padx=10, pady=10)
entry_password = tk.Entry(registration_frame, show='*')
entry_password.grid(row=3, column=1, padx=10, pady=10)

register_button = tk.Button(registration_frame, text="Register", command=register, bg="#FF3399", fg="#FFFFFF", font=("Arial", 16))
register_button.grid(row=4, column=0, columnspan=2, pady=20)

# Create the Login tab
login_frame = ttk.Frame(notebook)
notebook.add(login_frame, text="Login", padding=10)

# Create and place labels and entry widgets for the Login form
tk.Label(login_frame, text="Email", bg="#333333", fg="#FFFFFF").grid(row=0, column=0, padx=10, pady=10)
login_entry_email = tk.Entry(login_frame)
login_entry_email.grid(row=0, column=1, padx=10, pady=10)

tk.Label(login_frame, text="Password", bg="#333333", fg="#FFFFFF").grid(row=1, column=0, padx=10, pady=10)
login_entry_password = tk.Entry(login_frame, show='*')
login_entry_password.grid(row=1, column=1, padx=10, pady=10)

login_button = tk.Button(login_frame, text="Login", command=login, bg="#FF3399", fg="#FFFFFF", font=("Arial", 16))
login_button.grid(row=2, column=0, columnspan=2, pady=20)

# Create the Diary tab
diary_frame = ttk.Frame(notebook)
notebook.add(diary_frame, text="Diary", padding=10)

# Create and place widgets for the Diary form
tk.Label(diary_frame, text="Title", bg="#333333", fg="#FFFFFF").grid(row=0, column=0, padx=10, pady=10)
diary_title_entry = tk.Entry(diary_frame)
diary_title_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(diary_frame, text="Content", bg="#333333", fg="#FFFFFF").grid(row=1, column=0, padx=10, pady=10)
diary_content_text = tk.Text(diary_frame, height=10, width=40)
diary_content_text.grid(row=1, column=1, padx=10, pady=10)

diary_add_button = tk.Button(diary_frame, text="Add", command=add_diary, bg="#FF3399", fg="#FFFFFF", font=("Arial", 16))
diary_add_button.grid(row=2, column=0, padx=10, pady=10)

diary_update_button = tk.Button(diary_frame, text="Update", command=update_diary, bg="#FF3399", fg="#FFFFFF", font=("Arial", 16))
diary_update_button.grid(row=2, column=1, padx=10, pady=10)

diary_delete_button = tk.Button(diary_frame, text="Delete", command=delete_diary, bg="#FF3399", fg="#FFFFFF", font=("Arial", 16))
diary_delete_button.grid(row=2, column=2, padx=10, pady=10)

# Create a treeview for displaying diary entries
diary_tree = ttk.Treeview(diary_frame, columns=("id", "title"), show="headings")
diary_tree.heading("id", text="ID")
diary_tree.heading("title", text="Title")
diary_tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Initialize the database
create_database()

# Run the application
app.mainloop()
