from datetime import datetime
from app import db
import logging

logger = logging.getLogger(__name__)

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
        """
        取得所有分類記錄
        :return: Category 物件的列表，失敗時回傳空列表
        """
        try:
            return cls.query.all()
        except Exception as e:
            logger.error(f"取得所有分類時發生錯誤: {e}")
            return []

    @classmethod
    def get_by_id(cls, category_id):
        """
        取得單筆分類記錄
        :param category_id: 分類 ID
        :return: Category 物件或 None
        """
        try:
            return cls.query.get(category_id)
        except Exception as e:
            logger.error(f"取得分類 {category_id} 時發生錯誤: {e}")
            return None

    @classmethod
    def create(cls, name):
        """
        新增一筆分類記錄
        :param name: 分類名稱
        :return: 新增的 Category 物件或 None (如果失敗)
        """
        try:
            category = cls(name=name)
            db.session.add(category)
            db.session.commit()
            return category
        except Exception as e:
            db.session.rollback()
            logger.error(f"建立分類時發生錯誤: {e}")
            return None


class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    @classmethod
    def get_all(cls):
        """
        取得所有標籤記錄
        :return: Tag 物件的列表，失敗時回傳空列表
        """
        try:
            return cls.query.all()
        except Exception as e:
            logger.error(f"取得所有標籤時發生錯誤: {e}")
            return []

    @classmethod
    def get_by_id(cls, tag_id):
        """
        取得單筆標籤記錄
        :param tag_id: 標籤 ID
        :return: Tag 物件或 None
        """
        try:
            return cls.query.get(tag_id)
        except Exception as e:
            logger.error(f"取得標籤 {tag_id} 時發生錯誤: {e}")
            return None

    @classmethod
    def create(cls, name):
        """
        新增一筆標籤記錄
        :param name: 標籤名稱
        :return: 新增的 Tag 物件或 None (如果失敗)
        """
        try:
            tag = cls(name=name)
            db.session.add(tag)
            db.session.commit()
            return tag
        except Exception as e:
            db.session.rollback()
            logger.error(f"建立標籤時發生錯誤: {e}")
            return None


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
        """
        取得所有食譜記錄
        :return: Recipe 物件的列表，失敗時回傳空列表
        """
        try:
            return cls.query.all()
        except Exception as e:
            logger.error(f"取得食譜列表發生錯誤: {e}")
            return []

    @classmethod
    def get_by_id(cls, recipe_id):
        """
        取得單筆食譜記錄
        :param recipe_id: 食譜 ID
        :return: Recipe 物件或 None
        """
        try:
            return cls.query.get(recipe_id)
        except Exception as e:
            logger.error(f"取得食譜 {recipe_id} 時發生錯誤: {e}")
            return None
        
    @classmethod
    def create(cls, title, ingredients, steps, category_id, cooking_time=None, tags=None):
        """
        新增一筆食譜記錄
        :param title: 食譜名稱 (必填)
        :param ingredients: 所需食材 (必填)
        :param steps: 料理步驟 (必填)
        :param category_id: 所屬分類 ID (必填)
        :param cooking_time: 料理時間
        :param tags: 關聯的 Tag 物件清單
        :return: 新增的 Recipe 物件或 None (如果失敗)
        """
        try:
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
        except Exception as e:
            db.session.rollback()
            logger.error(f"建立食譜時發生錯誤: {e}")
            return None

    def update(self, title=None, ingredients=None, steps=None, cooking_time=None, category_id=None, tags=None):
        """
        更新單筆食譜記錄
        :param title: 食譜名稱
        :param ingredients: 所需食材
        :param steps: 料理步驟
        :param cooking_time: 料理時間
        :param category_id: 所屬分類 ID
        :param tags: 關聯的 Tag 物件清單
        :return: 更新的 Recipe 物件或 None (如果失敗)
        """
        try:
            if title is not None: self.title = title
            if ingredients is not None: self.ingredients = ingredients
            if steps is not None: self.steps = steps
            if cooking_time is not None: self.cooking_time = cooking_time
            if category_id is not None: self.category_id = category_id
            if tags is not None: self.tags = tags
            
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            logger.error(f"更新食譜 {self.id} 時發生錯誤: {e}")
            return None

    def delete(self):
        """
        刪除單筆食譜記錄
        :return: True (成功) 或 False (失敗)
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"刪除食譜 {self.id} 時發生錯誤: {e}")
            return False
