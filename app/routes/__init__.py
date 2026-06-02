from flask import Flask
from .main import main_bp
from .auth import auth_bp
from .logs import logs_bp
from .analysis import analysis_bp

def register_blueprints(app: Flask):
    """
    註冊主應用程式中的所有 Flask Blueprint (功能模組路由)。
    
    包含：
    - main_bp: 首頁與 Dashboard 頁面 (/)
    - auth_bp: 使用者註冊、登入、登出認證頁面 (/auth)
    - logs_bp: 排便日誌的 CRUD 操作頁面 (/logs)
    - analysis_bp: 單次布里斯托分析與綜合飲食建議頁面 (/analysis)
    
    Args:
        app (Flask): Flask 應用程式實例
    """
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(logs_bp, url_prefix='/logs')
    app.register_blueprint(analysis_bp, url_prefix='/analysis')
