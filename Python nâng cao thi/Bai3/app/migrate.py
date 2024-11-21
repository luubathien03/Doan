from app import db, app

# Chạy trong app context
with app.app_context():
    # Bước 1: Tạo một bảng mới không có avatar
    db.engine.execute('''
        CREATE TABLE new_student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            class_name TEXT NOT NULL
        );
    ''')

    # Bước 2: Chuyển dữ liệu từ bảng cũ sang bảng mới
    db.engine.execute('''
        INSERT INTO new_student (id, name, age, class_name)
        SELECT id, name, age, class_name FROM student;
    ''')

    # Bước 3: Xóa bảng cũ
    db.engine.execute('DROP TABLE student;')

    # Bước 4: Đổi tên bảng mới thành tên bảng cũ
    db.engine.execute('ALTER TABLE new_student RENAME TO student;')
