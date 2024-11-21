from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Khởi tạo đối tượng Flask và SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # Thay đổi nếu bạn sử dụng DB khác
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Khởi tạo db
db = SQLAlchemy(app)

# Sau khi db được khởi tạo, bạn có thể import các mô-đun khác của ứng dụng
from app import routes, models
