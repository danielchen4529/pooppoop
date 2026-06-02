from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Dashboard 首頁。
    
    業務邏輯：
    - 檢查 session['user_id'] 是否存在以判斷登入狀態。
    - 若已登入：
      1. 呼叫 User.get_by_id() 查詢當前使用者。
      2. 查詢該使用者最近的排便紀錄 (如 3-5 筆) 傳遞至首頁。
      3. 計算本週排便次數與最常出現的布里斯托類型，提供 Dashboard 卡片呈現。
      4. 準備 Chart.js 所需之圓餅圖與長條圖數據。
    - 若未登入（訪客）：
      1. 顯示基本的功能介紹與登入/註冊按鈕。
    
    回傳：
      - 渲染 'index.html' 模板。
    """
    # 骨架程式碼只保留 return，之後由實作階段補上
    # return render_template('index.html')
    pass
