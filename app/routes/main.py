from flask import Blueprint, render_template, session, redirect, url_for
from app.models import User, PoopLog
from datetime import datetime, timedelta
from collections import Counter

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Dashboard 首頁。
    
    業務邏輯：
    - 檢查 session['user_id'] 是否存在以判斷登入狀態。
    - 若已登入：
      1. 呼叫 User.get_by_id() 查詢當前使用者。
      2. 查詢該使用者最近的排便紀錄 (如 5 筆) 傳遞至首頁。
      3. 計算本週排便次數與最常出現的布里斯托類型，提供 Dashboard 看板呈現。
      4. 準備 Chart.js 所需之圓餅圖與長條圖數據。
    - 若未登入（訪客）：
      1. 顯示基本的功能介紹與登入/註冊按鈕。
    
    回傳：
      - 渲染 'index.html' 模板。
    """
    user_id = session.get('user_id')
    if user_id:
        user = User.get_by_id(user_id)
        if not user:
            # Session 中的 user_id 在資料庫中不存在，清除 session
            session.pop('user_id', None)
            return redirect(url_for('main.index'))
            
        # 取得該使用者的所有排便記錄
        all_logs = PoopLog.get_all(user_id=user.id)
        recent_logs = all_logs[:5]
        
        # 統計本週（過去 7 天內）的排便次數
        now = datetime.utcnow()
        seven_days_ago = now - timedelta(days=7)
        week_logs = [log for log in all_logs if log.date_time >= seven_days_ago]
        week_count = len(week_logs)
        
        # 統計最常出現的布里斯托類型
        bristol_types = [log.bristol_type for log in all_logs]
        if bristol_types:
            most_common_type = Counter(bristol_types).most_common(1)[0][0]
        else:
            most_common_type = "無記錄"
            
        # 統計各布里斯托類型的分布（用於 Chart.js 圓餅圖）
        type_distribution = [0] * 7 # 索引 0-6 對應 Type 1-7
        for t in bristol_types:
            if 1 <= t <= 7:
                type_distribution[t-1] += 1
                
        return render_template(
            'index.html', 
            user=user, 
            recent_logs=recent_logs,
            total_count=len(all_logs),
            week_count=week_count,
            most_common_type=most_common_type,
            type_distribution=type_distribution
        )
        
    return render_template('index.html', user=None)
