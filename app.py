import os
from flask import Flask
from app import db
from app.routes.main import main_bp
from app.routes.recipe import recipe_bp

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # 基本設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # 設定 SQLite 資料庫路徑 (指向 instance/database.db)
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'instance', 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', f'sqlite:///{db_path}')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化套件
    db.init_app(app)

    # 註冊 Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(recipe_bp)

    return app

app = create_app()

if __name__ == '__main__':
    # 確保 instance 目錄存在
    if not os.path.exists('instance'):
        os.makedirs('instance')
        
    app.run(debug=True, port=5000)
