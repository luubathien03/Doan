from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Đường dẫn đến thư mục lưu trữ ảnh
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Chỉ cho phép những định dạng file ảnh nhất định
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Mô hình cơ sở dữ liệu học sinh
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.String(120), nullable=True)  # Tên ảnh

    def __repr__(self):
        return f'<Student {self.name}>'

# Kiểm tra định dạng file ảnh hợp lệ
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        class_name = request.form['class_name']
        avatar = request.files['avatar']

        # Xử lý ảnh nếu có
        avatar_filename = None
        if avatar and allowed_file(avatar.filename):
            avatar_filename = secure_filename(avatar.filename)
            avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename))

        # Tạo đối tượng học sinh mới và lưu vào cơ sở dữ liệu
        new_student = Student(name=name, age=age, class_name=class_name, avatar=avatar_filename)
        db.session.add(new_student)
        db.session.commit()

        return redirect('/')

    return render_template('add_student.html')

if __name__ == '__main__':
    app.run(debug=True)
