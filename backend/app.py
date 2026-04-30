import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from models import db
from routes import api


def create_app():
    app = Flask(__name__)
    app.secret_key = "interview-bank-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///interview_bank.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app)
    db.init_app(app)

    app.register_blueprint(api, url_prefix="/api")

    with app.app_context():
        db.create_all()
        init_default_data()

    return app


def init_default_data():
    from models.user import User
    from models.category import Category

    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", is_admin=1)
        admin.set_password("admin123")
        db.session.add(admin)

    default_categories = [
        ("Java八股", "八股"),
        ("操作系统", "八股"),
        ("计算机网络", "八股"),
        ("数据库", "八股"),
        ("大模型agent", "八股"),
        ("算法", "算法"),
        ("C++", "代码"),
        ("Java", "代码"),
        ("Python", "代码"),
    ]
    for name, qtype in default_categories:
        if not Category.query.filter_by(name=name).first():
            c = Category(name=name, type=qtype)
            db.session.add(c)

    db.session.commit()
    print("Database initialized!")


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
