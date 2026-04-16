from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models.recipe import Recipe, Category, Tag

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

@recipe_bp.route('/search', methods=['GET'])
def search_recipes():
    """
    搜尋與篩選食譜
    """
    keyword = request.args.get('q', '').strip()
    category_id = request.args.get('category_id')
    
    # 建立查詢條件
    query = Recipe.query
    if keyword:
        # 使用 ilike 進行不區分大小寫的模糊比對
        query = query.filter(Recipe.title.ilike(f'%{keyword}%'))
    if category_id and category_id.isdigit():
        query = query.filter(Recipe.category_id == int(category_id))
        
    recipes = query.all()
    categories = Category.get_all()
    
    return render_template(
        'index.html', 
        recipes=recipes, 
        categories=categories, 
        keyword=keyword, 
        selected_category_id=category_id
    )

@recipe_bp.route('/new', methods=['GET', 'POST'])
def create_recipe():
    """
    新增食譜
    """
    categories = Category.get_all()
    tags = Tag.get_all()

    if request.method == 'POST':
        # 1. 抓取表單資料
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        cooking_time = request.form.get('cooking_time')
        category_id = request.form.get('category_id')
        selected_tag_ids = request.form.getlist('tag_ids') # list of strings

        # 2. 資料驗證
        if not title or not ingredients or not steps or not category_id:
            flash("標題、食材、步驟與分類皆為必填欄位！", "danger")
            return render_template('form.html', categories=categories, tags=tags, recipe=None, default_tags=[])

        # 處理資料轉型
        cooking_time_val = int(cooking_time) if cooking_time and cooking_time.isdigit() else None
        
        # 將標籤 ID 轉換為 Model 物件
        tag_objects = []
        if selected_tag_ids:
            for tid in selected_tag_ids:
                if tid.isdigit():
                    tag_obj = Tag.get_by_id(int(tid))
                    if tag_obj:
                        tag_objects.append(tag_obj)

        # 3. 呼叫 Model 存檔
        new_recipe = Recipe.create(
            title=title.strip(),
            ingredients=ingredients.strip(),
            steps=steps.strip(),
            category_id=int(category_id),
            cooking_time=cooking_time_val,
            tags=tag_objects
        )
        
        # 4. 成功後 redirect
        if new_recipe:
            flash("食譜新增成功！", "success")
            return redirect(url_for('recipe.detail', recipe_id=new_recipe.id))
        else:
            flash("系統發生錯誤，新增失敗請稍後再試。", "danger")

    # 若為 GET，直接渲染空白表單
    return render_template('form.html', categories=categories, tags=tags, recipe=None, default_tags=[])

@recipe_bp.route('/<int:recipe_id>', methods=['GET'])
def detail(recipe_id):
    """
    檢視食譜詳細資料
    """
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        abort(404) # 找不到該則食譜
        
    return render_template('detail.html', recipe=recipe)

@recipe_bp.route('/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    """
    編輯食譜
    """
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        abort(404)
        
    categories = Category.get_all()
    tags = Tag.get_all()

    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        cooking_time = request.form.get('cooking_time')
        category_id = request.form.get('category_id')
        selected_tag_ids = request.form.getlist('tag_ids')

        # 基本防呆驗證
        if not title or not ingredients or not steps or not category_id:
            flash("標題、食材、步驟與分類皆為必填欄位！", "danger")
            default_tags = [t.id for t in recipe.tags]
            return render_template('form.html', categories=categories, tags=tags, recipe=recipe, default_tags=default_tags)

        cooking_time_val = int(cooking_time) if cooking_time and cooking_time.isdigit() else None
        
        tag_objects = []
        if selected_tag_ids:
            for tid in selected_tag_ids:
                if tid.isdigit():
                    tag_obj = Tag.get_by_id(int(tid))
                    if tag_obj:
                        tag_objects.append(tag_obj)

        updated_recipe = recipe.update(
            title=title.strip(),
            ingredients=ingredients.strip(),
            steps=steps.strip(),
            category_id=int(category_id),
            cooking_time=cooking_time_val,
            tags=tag_objects
        )
        
        if updated_recipe:
            flash("食譜更新成功！", "success")
            return redirect(url_for('recipe.detail', recipe_id=recipe.id))
        else:
            flash("更新失敗，請稍後再試。", "danger")

    # 針對 GET request：預先填入當前所選的 tag_ids
    default_tags = [t.id for t in recipe.tags]
    return render_template('form.html', categories=categories, tags=tags, recipe=recipe, default_tags=default_tags)

@recipe_bp.route('/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    刪除食譜
    """
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        abort(404)
        
    if recipe.delete():
        flash(f"已成功刪除食譜：{recipe.title}", "success")
    else:
        flash("刪除食譜時發生錯誤。", "danger")
        
    return redirect(url_for('main.index'))
