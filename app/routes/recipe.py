from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models.recipe import Recipe, Category, Tag

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

@recipe_bp.route('/search', methods=['GET'])
def search_recipes():
    """
    搜尋與篩選食譜
    處理邏輯:
    1. 取得 request.args.get('q') 或其他條件
    2. 依據條件拼裝 SQLAlchemy Filter
    3. 傳遞給 index.html 渲染，並在介面上表示「搜尋結果」
    """
    pass

@recipe_bp.route('/new', methods=['GET', 'POST'])
def create_recipe():
    """
    新增食譜
    處理邏輯:
    - GET: 取出分類與標籤選項，並顯示空白 form.html 
    - POST: 
      1. 抓取表單資料 (request.form)
      2. 資料驗證，缺少時顯示 flash()
      3. 呼叫 Recipe.create() 存檔
      4. 成功後 redirect 到 /recipes/<新id>
    """
    pass

@recipe_bp.route('/<int:recipe_id>', methods=['GET'])
def detail(recipe_id):
    """
    檢視食譜詳細資料
    處理邏輯:
    1. 執行 Recipe.query.get_or_404(recipe_id)
    2. 渲染並丟入 detail.html
    """
    pass

@recipe_bp.route('/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    """
    編輯食譜
    處理邏輯:
    - 先抓取目標原本資料 (get_or_404)
    - GET: 將舊資料傳入 rendering 的 form.html 中
    - POST: 走表單驗證並呼叫 recipe.update()
    - 成功後 redirect 回原先的 /recipes/<id> 頁面
    """
    pass

@recipe_bp.route('/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    刪除食譜
    處理邏輯:
    1. 注意：使用 POST 接收來自前端表單的回應
    2. 取得目標物件後執行 recipe.delete()
    3. delete() 內包含 DB session 機制
    4. 導向首頁 main.index
    """
    pass
