import os
from app import create_app

# 建立 Flask app 實例
app = create_app()

if __name__ == '__main__':
    # 取得連接埠與主機設定，預設為 localhost:5000
    host = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    debug = app.config.get('DEBUG', True)
    
    app.run(host=host, port=port, debug=debug)
