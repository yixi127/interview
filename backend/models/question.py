from . import db
from datetime import datetime


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), default="八股")
    category = db.Column(db.String(100))
    importance = db.Column(db.Integer, default=2)
    answer = db.Column(db.Text)
    is_archived = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "category": self.category,
            "importance": self.importance,
            "answer": self.answer,
            "is_archived": self.is_archived,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }
