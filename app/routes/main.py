from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models.recipe import Recipe, Category, Tag

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁 / 食譜總覽
    處理邏輯:
    1. 從資料庫撈取所有 Recipe
    2. 從資料庫撈取所有 Category 提供給側邊欄或選單
    3. 將資料丟往 render_template('index.html', recipes=...)
    """
    pass
