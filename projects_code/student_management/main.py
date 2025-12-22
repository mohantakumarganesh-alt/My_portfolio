import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1350x700+0+0")
        
        title = tk.Label(self.root, text="Student Management System", bd=10, relief=tk.GROOVE, font=("times new roman", 40, "bold"), bg="yellow", fg="red")
        title.pack(side=tk.TOP, fill=tk.X)
        
        # Variables
        self.Roll_No_var = tk.StringVar()
        self.Name_var = tk.StringVar()
        self.Email_var = tk.StringVar()
        self.Gender_var = tk.StringVar()
        self.Contact_var = tk.StringVar()
        self.Dob_var = tk.StringVar()
        self.Search_By = tk.StringVar()
        self.Search_Txt = tk.StringVar()
        
        # Manage Frame
        Manage_Frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="crimson")
        Manage_Frame.place(x=20, y=100, width=450, height=580)
        
        m_title = tk.Label(Manage_Frame, text="Manage Students", bg="crimson", fg="white", font=("times new roman", 30, "bold"))
        m_title.grid(row=0, columnspan=2, pady=20)
        
        lbl_roll = tk.Label(Manage_Frame, text="Roll No.", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_roll.grid(row=1, column=0, pady=10, padx=20, sticky="w")
        txt_roll = tk.Entry(Manage_Frame, textvariable=self.Roll_No_var, font=("times new roman", 15, "bold"), bd=5, relief=tk.GROOVE)
        txt_roll.grid(row=1, column=1, pady=10, padx=20, sticky="w")
        
        lbl_name = tk.Label(Manage_Frame, text="Name", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_name.grid(row=2, column=0, pady=10, padx=20, sticky="w")
        txt_name = tk.Entry(Manage_Frame, textvariable=self.Name_var, font=("times new roman", 15, "bold"), bd=5, relief=tk.GROOVE)
        txt_name.grid(row=2, column=1, pady=10, padx=20, sticky="w")
        
        lbl_email = tk.Label(Manage_Frame, text="Email", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_email.grid(row=3, column=0, pady=10, padx=20, sticky="w")
        txt_email = tk.Entry(Manage_Frame, textvariable=self.Email_var, font=("times new roman", 15, "bold"), bd=5, relief=tk.GROOVE)
        txt_email.grid(row=3, column=1, pady=10, padx=20, sticky="w")
        
        lbl_gender = tk.Label(Manage_Frame, text="Gender", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_gender.grid(row=4, column=0, pady=10, padx=20, sticky="w")
        combo_gender = ttk.Combobox(Manage_Frame, textvariable=self.Gender_var, font=("times new roman", 13, "bold"), state='readonly')
        combo_gender['values'] = ("Male", "Female", "Other")
        combo_gender.grid(row=4, column=1, pady=10, padx=20)
        
        lbl_contact = tk.Label(Manage_Frame, text="Contact", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_contact.grid(row=5, column=0, pady=10, padx=20, sticky="w")
        txt_contact = tk.Entry(Manage_Frame, textvariable=self.Contact_var, font=("times new roman", 15, "bold"), bd=5, relief=tk.GROOVE)
        txt_contact.grid(row=5, column=1, pady=10, padx=20, sticky="w")
        
        lbl_dob = tk.Label(Manage_Frame, text="D.O.B", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_dob.grid(row=6, column=0, pady=10, padx=20, sticky="w")
        txt_dob = tk.Entry(Manage_Frame, textvariable=self.Dob_var, font=("times new roman", 15, "bold"), bd=5, relief=tk.GROOVE)
        txt_dob.grid(row=6, column=1, pady=10, padx=20, sticky="w")
        
        lbl_address = tk.Label(Manage_Frame, text="Address", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_address.grid(row=7, column=0, pady=10, padx=20, sticky="w")
        self.txt_address = tk.Text(Manage_Frame, width=30, height=3, font=("times new roman", 10, "bold"))
        self.txt_address.grid(row=7, column=1, pady=10, padx=20, sticky="w")
        
        # Button Frame
        btn_Frame = tk.Frame(Manage_Frame, bd=4, relief=tk.RIDGE, bg="crimson")
        btn_Frame.place(x=15, y=500, width=420)
        
        Addbtn = tk.Button(btn_Frame, text="Add", width=10, command=self.add_student).grid(row=0, column=0, padx=10, pady=10)
        Updatebtn = tk.Button(btn_Frame, text="Update", width=10, command=self.update_data).grid(row=0, column=1, padx=10, pady=10)
        Deletebtn = tk.Button(btn_Frame, text="Delete", width=10, command=self.delete_data).grid(row=0, column=2, padx=10, pady=10)
        Clearbtn = tk.Button(btn_Frame, text="Clear", width=10, command=self.clear).grid(row=0, column=3, padx=10, pady=10)
        
        # Detail Frame
        Detail_Frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="crimson")
        Detail_Frame.place(x=500, y=100, width=800, height=580)
        
        lbl_search = tk.Label(Detail_Frame, text="Search By", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_search.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        
        combo_search = ttk.Combobox(Detail_Frame, textvariable=self.Search_By, width=10, font=("times new roman", 13, "bold"), state='readonly')
        combo_search['values'] = ("Roll_No", "Name", "Contact")
        combo_search.grid(row=0, column=1, pady=10, padx=20)
        
        txt_search = tk.Entry(Detail_Frame, textvariable=self.Search_Txt, width=20, font=("times new roman", 10, "bold"), bd=5, relief=tk.GROOVE)
        txt_search.grid(row=0, column=2, pady=10, padx=20, sticky="w")
        
        searchbtn = tk.Button(Detail_Frame, text="Search", width=10, pady=5, command=self.search_data).grid(row=0, column=3, padx=10, pady=10)
        showallbtn = tk.Button(Detail_Frame, text="Show All", width=10, pady=5, command=self.fetch_data).grid(row=0, column=4, padx=10, pady=10)
        
        # Table Frame
        Table_Frame = tk.Frame(Detail_Frame, bd=4, relief=tk.RIDGE, bg="crimson")
        Table_Frame.place(x=10, y=70, width=760, height=500)
        
        scroll_x = tk.Scrollbar(Table_Frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(Table_Frame, orient=tk.VERTICAL)
        self.Student_table = ttk.Treeview(Table_Frame, columns=("roll", "name", "email", "gender", "contact", "dob", "Address"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.config(command=self.Student_table.xview)
        scroll_y.config(command=self.Student_table.yview)
        
        self.Student_table.heading("roll", text="Roll No.")
        self.Student_table.heading("name", text="Name")
        self.Student_table.heading("email", text="Email")
        self.Student_table.heading("gender", text="Gender")
        self.Student_table.heading("contact", text="Contact")
        self.Student_table.heading("dob", text="D.O.B")
        self.Student_table.heading("Address", text="Address")
        self.Student_table['show'] = 'headings'
        self.Student_table.column("roll", width=100)
        self.Student_table.column("name", width=100)
        self.Student_table.column("email", width=100)
        self.Student_table.column("gender", width=100)
        self.Student_table.column("contact", width=100)
        self.Student_table.column("dob", width=100)
        self.Student_table.column("Address", width=150)
        self.Student_table.pack(fill=tk.BOTH, expand=1)
        self.Student_table.bind("<ButtonRelease-1>", self.get_cursor)
        
        self.init_db()
        self.fetch_data()

    def init_db(self):
        con = sqlite3.connect(database="students.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS students(roll_no INTEGER PRIMARY KEY, name TEXT, email TEXT, gender TEXT, contact TEXT, dob TEXT, address TEXT)")
        con.commit()
        con.close()

    def add_student(self):
        if self.Roll_No_var.get() == "" or self.Name_var.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            con = sqlite3.connect(database="students.db")
            cur = con.cursor()
            cur.execute("insert into students values(?,?,?,?,?,?,?)", (self.Roll_No_var.get(), self.Name_var.get(), self.Email_var.get(), self.Gender_var.get(), self.Contact_var.get(), self.Dob_var.get(), self.txt_address.get('1.0', tk.END)))
            con.commit()
            self.fetch_data()
            self.clear()
            con.close()
            messagebox.showinfo("Success", "Record has been inserted")

    def fetch_data(self):
        con = sqlite3.connect(database="students.db")
        cur = con.cursor()
        cur.execute("select * from students")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.Student_table.delete(*self.Student_table.get_children())
            for row in rows:
                self.Student_table.insert('', tk.END, values=row)
            con.commit()
        con.close()

    def clear(self):
        self.Roll_No_var.set("")
        self.Name_var.set("")
        self.Email_var.set("")
        self.Gender_var.set("")
        self.Contact_var.set("")
        self.Dob_var.set("")
        self.txt_address.delete("1.0", tk.END)

    def get_cursor(self, ev):
        cursor_row = self.Student_table.focus()
        contents = self.Student_table.item(cursor_row)
        row = contents['values']
        self.Roll_No_var.set(row[0])
        self.Name_var.set(row[1])
        self.Email_var.set(row[2])
        self.Gender_var.set(row[3])
        self.Contact_var.set(row[4])
        self.Dob_var.set(row[5])
        self.txt_address.delete("1.0", tk.END)
        self.txt_address.insert(tk.END, row[6])

    def update_data(self):
        con = sqlite3.connect(database="students.db")
        cur = con.cursor()
        cur.execute("update students set name=?, email=?, gender=?, contact=?, dob=?, address=? where roll_no=?", (self.Name_var.get(), self.Email_var.get(), self.Gender_var.get(), self.Contact_var.get(), self.Dob_var.get(), self.txt_address.get('1.0', tk.END), self.Roll_No_var.get()))
        con.commit()
        self.fetch_data()
        self.clear()
        con.close()

    def delete_data(self):
        con = sqlite3.connect(database="students.db")
        cur = con.cursor()
        cur.execute("delete from students where roll_no=?", (self.Roll_No_var.get(),))
        con.commit()
        con.close()
        self.fetch_data()
        self.clear()

    def search_data(self):
        con = sqlite3.connect(database="students.db")
        cur = con.cursor()
        cur.execute("select * from students where " + str(self.Search_By.get()) + " LIKE '%" + str(self.Search_Txt.get()) + "%'")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.Student_table.delete(*self.Student_table.get_children())
            for row in rows:
                self.Student_table.insert('', tk.END, values=row)
            con.commit()
        con.close()

if __name__ == "__main__":
    root = tk.Tk()
    obj = StudentManagementSystem(root)
    root.mainloop()
