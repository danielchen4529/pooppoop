import os
from flask import Flask
from config import config_by_name
from app.models import db
from app.routes import register_blueprints

def create_app(config_name=None):
    """
    Flask 應用程式工廠。
    
    根據環境變數或傳入參數載入配置，初始化 SQLAlchemy，並註冊 Blueprint 路由。
    """
    if not config_name:
        config_name = os.environ.get('FLASK_ENV', 'development')
        
    app = Flask(__name__)
    
    # 載入配置
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))
    
    # 確保 instance 資料夾存在 (SQLite 資料庫儲存處)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    # 初始化 SQLAlchemy
    db.init_app(app)
    
    # 註冊 Blueprints
    register_blueprints(app)
    
    return app

def init_db():
    """
    初始化資料庫。建立所有在 models 中定義的資料表。
    """
    app = create_app()
    with app.app_context():
        db.create_all()
        print("資料庫初始化完成！已成功建立所有資料表。")
