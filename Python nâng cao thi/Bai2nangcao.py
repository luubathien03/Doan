import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Kết nối tới database
conn = sqlite3.connect('students.db')
c = conn.cursor()

# Kiểm tra và thêm cột 'enrollment_date' (ngày nhập học) và 'grade' (học lực) nếu chưa có
c.execute('''PRAGMA table_info(students)''')
columns = [column[1] for column in c.fetchall()]
if 'enrollment_date' not in columns:
    c.execute('''ALTER TABLE students ADD COLUMN enrollment_date TEXT''')  # Thêm cột enrollment_date
if 'grade' not in columns:
    c.execute('''ALTER TABLE students ADD COLUMN grade TEXT''')  # Thêm cột grade

# Tạo bảng nếu chưa tồn tại (cập nhật tên trường từ 'dob' thành 'enrollment_date' và 'address' thành 'grade')
c.execute('''CREATE TABLE IF NOT EXISTS students
             (id INTEGER PRIMARY KEY, name TEXT, enrollment_date TEXT, grade TEXT)''')

# Hàm thêm học sinh
def add_student(name, enrollment_date, grade):
    if not grade:
        grade = "None"  # Nếu không có học lực, set mặc định là "None"
    c.execute("INSERT INTO students (name, enrollment_date, grade) VALUES (?, ?, ?)", (name, enrollment_date, grade))
    conn.commit()

# Hàm cập nhật thông tin học sinh
def edit_student(student_id, name, enrollment_date, grade):
    if not grade:
        grade = "None"  # Nếu không có học lực, set mặc định là "None"
    c.execute("UPDATE students SET name = ?, enrollment_date = ?, grade = ? WHERE id = ?", (name, enrollment_date, grade, student_id))
    conn.commit()

# Hàm xoá học sinh
def delete_student(student_id):
    c.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()

# Hàm tìm kiếm học sinh
def search_students(name):
    c.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + name + '%',))
    return c.fetchall()

# Hàm hiển thị danh sách học sinh
def view_students():
    c.execute("SELECT * FROM students")
    return c.fetchall()

# Hàm đăng nhập
def login():
    username = entry_username.get()
    password = entry_password.get()
    if username == "admin" and password == "admin":
        login_window.destroy()
        main_window()
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password")

# Giao diện quản lý học sinh
def main_window():
    root = Tk()
    root.title("Student Management")
    root.geometry("700x500")
    root.config(bg="#F2F2F2")

    # Hàm xử lý thêm học sinh
    def add_student_gui():
        name = entry_name.get()
        enrollment_date = entry_enrollment_date.get()
        grade = entry_grade.get()
        if name and enrollment_date:
            add_student(name, enrollment_date, grade)
            entry_name.delete(0, END)
            entry_enrollment_date.delete(0, END)
            entry_grade.delete(0, END)
            view_students_gui()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    # Hàm hiển thị danh sách học sinh
    def view_students_gui():
        students = view_students()
        for row in tree.get_children():
            tree.delete(row)
        for student in students:
            # Đảm bảo hiển thị chuỗi trống nếu không có học lực
            grade_value = student[3] if student[3] else ""
            tree.insert('', 'end', iid=student[0], values=(student[1], student[2], grade_value))

    # Hàm tìm kiếm học sinh
    def search_students_gui():
        name = entry_search.get()
        students = search_students(name)
        for row in tree.get_children():
            tree.delete(row)
        for student in students:
            # Đảm bảo hiển thị chuỗi trống nếu không có học lực
            grade_value = student[3] if student[3] else ""
            tree.insert('', 'end', iid=student[0], values=(student[1], student[2], grade_value))

    # Hàm mở cửa sổ chỉnh sửa học sinh
    def edit_window():
        selected = tree.selection()
        if selected:
            student_id = selected[0]  # Lấy ID từ selection của treeview
            student_name = tree.item(selected[0])['values'][0]
            student_enrollment_date = tree.item(selected[0])['values'][1]
            student_grade = tree.item(selected[0])['values'][2]
            edit_student_gui(student_id, student_name, student_enrollment_date, student_grade)
        else:
            messagebox.showwarning("Select Student", "Please select a student to edit.")

    # Tạo cửa sổ chỉnh sửa học sinh
    def edit_student_gui(student_id, student_name, student_enrollment_date, student_grade):
        window = Toplevel(root)
        window.title(f"Edit {student_name}")
        window.geometry("300x250")
        window.config(bg="#F2F2F2")

        Label(window, text="Name", font=("Arial", 12), bg="#F2F2F2").grid(row=0, column=0, pady=10, padx=10)
        Label(window, text="Enrollment Date", font=("Arial", 12), bg="#F2F2F2").grid(row=1, column=0, pady=10, padx=10)
        Label(window, text="Grade", font=("Arial", 12), bg="#F2F2F2").grid(row=2, column=0, pady=10, padx=10)

        entry_name_edit = Entry(window, font=("Arial", 12))
        entry_enrollment_date_edit = Entry(window, font=("Arial", 12))
        entry_grade_edit = Entry(window, font=("Arial", 12))

        entry_name_edit.grid(row=0, column=1, pady=10, padx=10)
        entry_enrollment_date_edit.grid(row=1, column=1, pady=10, padx=10)
        entry_grade_edit.grid(row=2, column=1, pady=10, padx=10)

        # Set initial values
        entry_name_edit.insert(0, student_name)
        entry_enrollment_date_edit.insert(0, student_enrollment_date)
        entry_grade_edit.insert(0, student_grade)

        def save_edit():
            name = entry_name_edit.get()
            enrollment_date = entry_enrollment_date_edit.get()
            grade = entry_grade_edit.get()
            if name and enrollment_date:
                edit_student(student_id, name, enrollment_date, grade)
                view_students_gui()
                window.destroy()
            else:
                messagebox.showwarning("Input Error", "Please fill all fields.")

        Button(window, text="Save", command=save_edit, font=("Arial", 12), bg="#4CAF50", fg="white").grid(row=3, column=1, pady=10, padx=10)

    # Hàm xóa học sinh
    def delete_student_gui():
        selected = tree.selection()
        if selected:
            student_id = selected[0]  # Lấy ID từ selection của treeview
            delete_student(student_id)
            view_students_gui()  # Cập nhật lại Treeview
        else:
            messagebox.showwarning("Select Student", "Please select a student to delete.")

    # Các widget cho giao diện chính
    Label(root, text="Name", font=("Arial", 12), bg="#F2F2F2").grid(row=0, column=0, pady=10, padx=10)
    Label(root, text="Enrollment Date", font=("Arial", 12), bg="#F2F2F2").grid(row=1, column=0, pady=10, padx=10)
    Label(root, text="Grade", font=("Arial", 12), bg="#F2F2F2").grid(row=2, column=0, pady=10, padx=10)
    Label(root, text="Search by Name", font=("Arial", 12), bg="#F2F2F2").grid(row=3, column=0, pady=10, padx=10)

    entry_name = Entry(root, font=("Arial", 12))
    entry_enrollment_date = Entry(root, font=("Arial", 12))
    entry_grade = Entry(root, font=("Arial", 12))
    entry_search = Entry(root, font=("Arial", 12))

    entry_name.grid(row=0, column=1, pady=10, padx=10)
    entry_enrollment_date.grid(row=1, column=1, pady=10, padx=10)
    entry_grade.grid(row=2, column=1, pady=10, padx=10)
    entry_search.grid(row=3, column=1, pady=10, padx=10)

    Button(root, text="Add Student", command=add_student_gui, font=("Arial", 12), bg="#4CAF50", fg="white").grid(row=4, column=0, pady=10, padx=10)
    Button(root, text="View Students", command=view_students_gui, font=("Arial", 12), bg="#2196F3", fg="white").grid(row=4, column=1, pady=10, padx=10)
    Button(root, text="Search", command=search_students_gui, font=("Arial", 12), bg="#FFC107", fg="white").grid(row=3, column=2, pady=10, padx=10)
    Button(root, text="Edit", command=edit_window, font=("Arial", 12), bg="#4CAF50", fg="white").grid(row=5, column=0, pady=10, padx=10)
    Button(root, text="Delete", command=delete_student_gui, font=("Arial", 12), bg="#F44336", fg="white").grid(row=5, column=1, pady=10, padx=10)

    # Treeview for students
    columns = ('Name', 'Enrollment Date', 'Grade')
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.grid(row=6, column=0, columnspan=3, pady=20, padx=10)

    for col in columns:
        tree.heading(col, text=col, anchor=CENTER)
        tree.column(col, anchor=CENTER, width=150)

    view_students_gui()
    root.mainloop()

# Giao diện đăng nhập
login_window = Tk()
login_window.title("Login")
login_window.geometry("300x200")
login_window.config(bg="#F2F2F2")

Label(login_window, text="Username", font=("Arial", 12), bg="#F2F2F2").grid(row=0, column=0, pady=10, padx=10)
Label(login_window, text="Password", font=("Arial", 12), bg="#F2F2F2").grid(row=1, column=0, pady=10, padx=10)

entry_username = Entry(login_window, font=("Arial", 12))
entry_password = Entry(login_window, show="*", font=("Arial", 12))

entry_username.grid(row=0, column=1, pady=10, padx=10)
entry_password.grid(row=1, column=1, pady=10, padx=10)

Button(login_window, text="Login", command=login, font=("Arial", 12), bg="#4CAF50", fg="white").grid(row=2, column=1, pady=10)

login_window.mainloop()

# Đóng kết nối database khi hoàn thành
conn.close()
