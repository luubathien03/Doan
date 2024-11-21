from flask import Flask, render_template, request, redirect, url_for
from app import app, db
from app.models import Student

# Route hiển thị danh sách học sinh
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Route thêm học sinh mới
@app.route('/add', methods=['POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        class_name = request.form['class_name']
        
        # Tạo đối tượng học sinh mới
        new_student = Student(name=name, age=age, class_name=class_name)
        
        # Thêm học sinh vào cơ sở dữ liệu
        db.session.add(new_student)
        db.session.commit()
        
        return redirect(url_for('index'))

# Route xóa học sinh
@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

# Route chỉnh sửa thông tin học sinh
@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    
    if request.method == 'POST':
        student.name = request.form['name']
        student.age = request.form['age']
        student.class_name = request.form['class_name']
        
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit_student.html', student=student)
