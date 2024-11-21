from app import app, db
from app.models import Student

# Tạo tất cả bảng nếu chúng chưa có
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
