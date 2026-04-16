import os
from flask import Flask
from app import db
from app.models.recipe import Category, Tag, Recipe

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'database.db')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', f'sqlite:///{db_path}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    # 建立所有表單
    db.create_all()
    
    # 若沒有資料，預先填入實用的分類與標籤做為測試
    if not Category.query.first():
        db.session.add_all([
            Category(name='早餐'), 
            Category(name='午餐'), 
            Category(name='晚餐'), 
            Category(name='甜點'),
            Category(name='異國料理')
        ])
    if not Tag.query.first():
        db.session.add_all([
            Tag(name='低卡'), 
            Tag(name='快速'), 
            Tag(name='聚會用'), 
            Tag(name='高蛋白')
        ])
    
    db.session.commit()
    print("Database initialized.")
