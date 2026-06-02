from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models import PoopLog, DietSuggestion
from app.services import bristol, diet

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/<int:id>', methods=['GET'])
def view_result(id):
    """
    顯示單次排便記錄的分析結果。
    
    輸入：
    - URL 參數 id (記錄 ID)
    
    業務邏輯：
    1. 驗證登入狀態。
    2. 呼叫 PoopLog.get_by_id(id) 查詢該筆排便記錄。
    3. 若記錄不存在，回傳 404；若無存取權限，回傳 403。
    4. 呼叫服務層 app.services.bristol.analyze(log) 規則引擎進行分析。
    5. 渲染 'analysis/result.html'，傳入 log 與分析結果。
    """
    user_id = session.get('user_id')
    if not user_id:
        flash("請先登入系統以查看排便分析結果！", "error")
        return redirect(url_for('auth.login'))
        
    log = PoopLog.get_by_id(id)
    if not log:
        flash("該筆日誌紀錄不存在！", "error")
        return render_template('errors/404.html'), 404
        
    if log.user_id != user_id:
        flash("您無權限查看此分析結果！", "error")
        return render_template('errors/403.html'), 403
        
    # 呼叫布里斯托規則引擎進行分析
    result = bristol.analyze(log)
    return render_template('analysis/result.html', log=log, result=result)

@analysis_bp.route('/suggestion', methods=['GET'])
def view_suggestion():
    """
    顯示使用者的綜合飲食與健康改善建議。
    
    業務邏輯：
    1. 驗證登入狀態。
    2. 查詢該使用者最近 14 天內所有的排便記錄。
    3. 若歷史記錄筆數小於 3 筆，則在頁面上提示「記錄不足，請持續填寫日誌以獲得精準建議」。
    4. 若記錄足夠，呼叫服務層 app.services.diet.generate_suggestion(logs) 進行綜合分析。
    5. 取得飲食改善方針，包含建議攝取、應避免食品、飲水提醒等。
    6. （選用）將飲食建議結果儲存/快取至 DietSuggestion 資料表中。
    7. 渲染 'analysis/suggestion.html'。
    """
    user_id = session.get('user_id')
    if not user_id:
        flash("請先登入系統以取得飲食與健康建議！", "error")
        return redirect(url_for('auth.login'))
        
    # 查詢當前使用者的所有排便日誌
    logs = PoopLog.get_all(user_id=user_id)
    
    # 呼叫飲食建議規則引擎
    suggestion = diet.generate_suggestion(logs)
    
    # 若記錄大於等於 3 筆，可選擇快取至資料庫
    if len(logs) >= 3:
        try:
            # 建立快取記錄
            DietSuggestion.create(
                user_id=user_id,
                summary=suggestion['summary'],
                content=suggestion['trend']
            )
        except Exception as e:
            # 快取失敗不影響使用者瀏覽網頁，僅記錄日誌即可
            pass
            
    return render_template('analysis/suggestion.html', suggestion=suggestion, logs_count=len(logs))
