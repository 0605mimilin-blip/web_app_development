from datetime import datetime
from app import db

# 多對多關聯表：紀錄食譜與標籤的關係
recipe_tags = db.Table('recipe_tags',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    # 關聯關係：一個分類包含多個食譜
    recipes = db.relationship('Recipe', backref='category', lazy=True, cascade='all, delete-orphan')

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def create(cls, name):
        category = cls(name=name)
        db.session.add(category)
        db.session.commit()
        return category


class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def create(cls, name):
        tag = cls(name=name)
        db.session.add(tag)
        db.session.commit()
        return tag


class Recipe(db.Model):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    cooking_time = db.Column(db.Integer, nullable=True) # 單位：分鐘
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 多對多關聯：一個食譜對應多個標籤
    tags = db.relationship('Tag', secondary=recipe_tags, lazy='subquery',
                           backref=db.backref('recipes', lazy=True))

    @classmethod
    def get_all(cls):
        """取得所有食譜，包含關聯的分類與標籤"""
        return cls.query.all()

    @classmethod
    def get_by_id(cls, recipe_id):
        """根據 ID 取得單一食譜"""
        return cls.query.get(recipe_id)
        
    @classmethod
    def create(cls, title, ingredients, steps, category_id, cooking_time=None, tags=None):
        """新增食譜"""
        recipe = cls(
            title=title,
            ingredients=ingredients,
            steps=steps,
            cooking_time=cooking_time,
            category_id=category_id
        )
        if tags:
            recipe.tags = tags
            
        db.session.add(recipe)
        db.session.commit()
        return recipe

    def update(self, title=None, ingredients=None, steps=None, cooking_time=None, category_id=None, tags=None):
        """更新食譜內容"""
        if title: self.title = title
        if ingredients: self.ingredients = ingredients
        if steps: self.steps = steps
        if cooking_time is not None: self.cooking_time = cooking_time
        if category_id: self.category_id = category_id
        if tags is not None: self.tags = tags # list of Tag objects
        
        db.session.commit()
        return self

    def delete(self):
        """刪除食譜"""
        db.session.delete(self)
        db.session.commit()
