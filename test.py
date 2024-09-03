import sqlite3
from tkinter import Tk, Label, Entry, Button, Listbox, END, messagebox, Toplevel

# Function to initialize database
def init_db():
    conn = sqlite3.connect('sample.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert data into the database
def add_user():
    name = entry_name.get()
    age = entry_age.get()
    if name and age:
        conn = sqlite3.connect('sample.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
        conn.commit()
        conn.close()
        listbox_users.insert(END, f'{name} - {age}')
        entry_name.delete(0, END)
        entry_age.delete(0, END)
    else:
        messagebox.showwarning('Input Error', 'Please enter both name and age')

# Function to load data from the database
def load_users():
    listbox_users.delete(0, END)
    conn = sqlite3.connect('sample.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, age FROM users')
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        listbox_users.insert(END, f'{row[0]} - {row[1]}')

def on_lbselect(event):
    selected_index = listbox_users.curselection()
    if selected_index:
        selected_item = listbox_users.get(selected_index)
        name, age = selected_item.split(' - ')
        new_form = Toplevel(app)
        new_form.title("test")
        new_form.geometry("200x100+400+400")

        Label(new_form, text=name).place(x=10, y=10, width=50, height=25)
        entry = Label(new_form, bd=2, relief='groove', bg='red', fg='white', text=age)
        entry.place(x=60, y=10, width=100, height=25)

# Initialize the database
init_db()

# Set up the GUI
app = Tk()
app.title('Simple SQLite App')
app.geometry("400x300+200+200")

label_name = Label(app, text='Name:', justify='left')
label_name.place(x=10, y=10, width=100, height=30)

entry_name = Entry(app, bd=2, relief='groove')
entry_name.place(x=120, y=10, width=200, height=30)

label_age = Label(app, text='Age:', justify='left')
label_age.place(x=10, y=50, width=100, height=30)

entry_age = Entry(app, bd=2, relief='groove')
entry_age.place(x=120, y=50, width=200, height=30)

button_add = Button(app, text='Add User', command=add_user, bd=2, relief='groove')
button_add.place(x=10, y=90, width=100, height=30)

button_load = Button(app, text='Load Users', command=load_users, bd=2, relief='groove')
button_load.place(x=120, y=90, width=100, height=30)

listbox_users = Listbox(app, bd=2, relief='groove')
listbox_users.place(x=10, y=130, width=350, height=400)
listbox_users.bind('<Double-1>', on_lbselect)

# Start the GUI loop
app.mainloop()
