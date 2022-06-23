from datetime import datetime

from flask_login import UserMixin

from apps.app import db

class UserImage(db.Model):
    __tablename__ = "user_images"
    id = db.Column(db.Integer, primary_key=True)
    #user_idはusersのidカラムを外部キーとする
    user_id = db.Column(db.String, db.ForeignKey("users.id"))

    image_path = db.Column(db.String)
    is_detected = db.Column(db.Boolean, default = False)
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate=datetime.now)
