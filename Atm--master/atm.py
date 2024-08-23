from tkinter import *
from tkinter import messagebox
import mysql.connector

# MySQL Database connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",  # Update with your database host
        user="root",       # Update with your database username
        password="Abhi@2003",  # Update with your database password
        database="atm_service"  # Update with your database name
    )

# Create tables if they don't exist
def setup_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        pin INT PRIMARY KEY,
        name VARCHAR(255)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        user_pin INT,
        amount DECIMAL(10, 2),
        FOREIGN KEY (user_pin) REFERENCES users(pin)
    )
    """)
    conn.commit()
    conn.close()

setup_db()

h = Tk()
h.title("Bank Service")
h.geometry("655x655")
h.maxsize(width=650, height=650)
h.minsize(width=600, height=600)

# Registration window
def Tj():
    top = Toplevel()
    top.maxsize(width=650, height=650)
    top.minsize(width=640, height=600)
    head = Label(top, text="Welcome to REGISTRATION FORM ", bg="green", fg="white", font=("", 26)).pack()

    def submit():
        if en.get() == "" or en2.get() == "":
            messagebox.showwarning("warning", "Blank Invalid")
        else:
            pin = int(en.get())
            name = en2.get()
            
            conn = connect_to_db()
            cursor = conn.cursor()

            # Insert user into database
            cursor.execute("INSERT INTO users (pin, name) VALUES (%s, %s)", (pin, name))
            conn.commit()
            conn.close()

            messagebox.showinfo("info", "Congratulations, you are registered!")
            top.destroy()

    en = Entry(top, bd=2)
    en.place(x=160, y=150)
    pin_label = Label(top, text="Enter your PIN:")
    pin_label.place(x=20, y=150)

    en2 = Entry(top, bd=2)
    en2.place(x=160, y=200)
    name_label = Label(top, text="Enter your Name:")
    name_label.place(x=6, y=200)

    su = Button(top, text="SUBMIT", fg="green", command=submit)
    su.place(x=9, y=240)

# Cash deposit window
def depo():
    top2 = Toplevel()
    top2.maxsize(width=650, height=650)
    top2.minsize(width=640, height=600)
    head = Label(top2, text="Welcome to CASH DEPOSITE", bg="orange", fg="white", font=("", 26)).pack()

    ent5 = Entry(top2, bd=2)
    ent5.place(x=160, y=150)

    def amou():
        pin = int(ent5.get())
        amount = float(entvalue.get())
        
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE pin = %s", (pin,))
        user = cursor.fetchone()

        if user:
            cursor.execute("INSERT INTO transactions (user_pin, amount) VALUES (%s, %s)", (pin, amount))
            conn.commit()
            messagebox.showinfo("Success", "Money deposited successfully")
            textho.config(text=f"Welcome back Mr/Mrs: {user[1]}\nThanks for depositing money: {amount}")
        else:
            messagebox.showwarning("warning", "You are not a customer")
        
        conn.close()
        top2.destroy()

    pin_label = Label(top2, text="Enter the PIN:")
    pin_label.place(x=20, y=150)

    entvalue = Entry(top2, bd=2)
    entvalue.place(x=160, y=200)
    amount_label = Label(top2, text="Enter the Amount:")
    amount_label.place(x=6, y=200)

    su = Button(top2, text="SUBMIT", fg="green", command=amou)
    su.place(x=9, y=240)

    textho = Label(top2, fg="green")
    textho.place(x=170, y=400)

# Cash withdrawal window
def cash():
    top3 = Toplevel()
    top3.maxsize(width=650, height=650)
    top3.minsize(width=640, height=600)
    head = Label(top3, text="Welcome to CASH WITHDRAWAL", bg="purple", fg="white", font=("", 26)).pack()

    ent6 = Entry(top3, bd=2)
    ent6.place(x=160, y=150)

    def submitwith():
        pin = int(ent6.get())
        amount = float(entvalue1.get())

        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM transactions WHERE user_pin = %s", (pin,))
        transactions = cursor.fetchall()
        total_balance = sum(t[1] for t in transactions)

        if total_balance >= amount:
            cursor.execute("INSERT INTO transactions (user_pin, amount) VALUES (%s, %s)", (pin, -amount))
            conn.commit()
            cursor.execute("SELECT name FROM users WHERE pin = %s", (pin,))
            user_name = cursor.fetchone()[0]
            textho2.config(text=f"Welcome back Mr/Mrs: {user_name}\nWithdrawal amount: {amount}")
            messagebox.showinfo("Success", "Money withdrawn successfully")
        else:
            messagebox.showwarning("warning", "Insufficient balance")

        conn.close()
        top3.destroy()

    pin_label = Label(top3, text="Enter the PIN:")
    pin_label.place(x=20, y=150)

    entvalue1 = Entry(top3, bd=2)
    entvalue1.place(x=230, y=200)
    amount_label = Label(top3, text="Enter the Withdrawal Amount:")
    amount_label.place(x=9, y=200)

    su1 = Button(top3, text="SUBMIT", fg="green", command=submitwith)
    su1.place(x=9, y=240)

    textho2 = Label(top3, fg="green")
    textho2.place(x=170, y=400)

# Balance check window
def checkb():
    top4 = Toplevel()
    top4.maxsize(width=650, height=650)
    top4.minsize(width=640, height=600)
    head2 = Label(top4, text="Welcome to Balance Check Service", bg="pink", fg="white", font=("", 26)).pack()

    ent7 = Entry(top4, bd=2)
    ent7.place(x=160, y=150)

    def click():
        pin = int(ent7.get())

        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM transactions WHERE user_pin = %s", (pin,))
        transactions = cursor.fetchall()
        total_balance = sum(t[1] for t in transactions)

        cursor.execute("SELECT name FROM users WHERE pin = %s", (pin,))
        user_name = cursor.fetchone()[0]
        
        textho3.config(text=f"Welcome back Mr/Mrs: {user_name}\nYour balance is: {total_balance} Rupees")
        
        conn.close()

    pin_label = Label(top4, text="Enter the PIN:")
    pin_label.place(x=20, y=150)

    su1 = Button(top4, text="SUBMIT", fg="green", command=click)
    su1.place(x=9, y=240)

    textho3 = Label(top4, fg="green")
    textho3.place(x=170, y=400)

# Other GUI components
te = Frame(h)
te.pack(side=TOP)
Label(te, text="Welcome to the Service ATM", fg="white", font=("arial", 33), bg="blue").pack()

en = Frame(h)
en.pack()
war = StringVar()
en = Entry(en, bg="white", fg="black", bd=6, width=20, textvariable=war).pack()

bt = Button(text="Register yourself", bd=5, command=Tj)
bt.place(x=20, y=110)

bt = Button(text="Cash Deposit", bd=5, command=depo)
bt.place(x=450, y=110)

bt = Button(text="Cash Withdrawal", bd=5, command=cash)
bt.place(x=20, y=160)

bt = Button(text="Cash Balance", bd=5, command=checkb)
bt.place(x=450, y=160)

def ex():
    y = messagebox.askyesno("exit", "Do you want to exit ?")
    if y:
        h.destroy()

exit_button = Button(text="EXIT", bd=1, fg="red", command=ex)
exit_button

h.mainloop()
