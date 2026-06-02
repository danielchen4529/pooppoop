from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import PoopLog
from datetime import datetime

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/', methods=['GET'])
def list_logs():
    """
    歷史記錄列表。
    
    輸入：
    - request.args.get('start_date')  (格式: 'YYYY-MM-DD', 可選)
    - request.args.get('end_date')    (格式: 'YYYY-MM-DD', 可選)
    
    業務邏輯：
    1. 驗證登入狀態 (檢查 session['user_id'])。若未登入，重導向至 '/auth/login'。
    2. 解析 start_date 與 end_date 字串為 datetime.date/datetime 物件。
    3. 呼叫 PoopLog.get_all(user_id=current_user, start_date=..., end_date=...) 查詢記錄列表。
    4. 將紀錄清單渲染至 'logs/list.html' 模板。
    """
    user_id = session.get('user_id')
    if not user_id:
        flash("請先登入系統以查看排便日誌！", "error")
        return redirect(url_for('auth.login'))
        
    start_date_str = request.args.get('start_date', '')
    end_date_str = request.args.get('end_date', '')
    
    start_date = None
    end_date = None
    
    try:
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        if end_date_str:
            # 設定結束時間為當天的 23:59:59
            end_date = datetime.strptime(end_date_str + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
    except ValueError:
        flash("日期篩選格式不正確，請使用 YYYY-MM-DD 格式！", "warning")
        
    logs = PoopLog.get_all(user_id=user_id, start_date=start_date, end_date=end_date)
    return render_template(
        'logs/list.html', 
        logs=logs, 
        start_date=start_date_str, 
        end_date=end_date_str
    )

@logs_bp.route('/new', methods=['GET'])
def new_log():
    """
    顯示新增記錄表單頁面。
    
    業務邏輯：
    - 驗證登入狀態。
    - 渲染 'logs/new.html' 模板。預設時間設為當前時間（ISO 格式）。
    """
    user_id = session.get('user_id')
    if not user_id:
        flash("請先登入以新增排便日誌！", "error")
        return redirect(url_for('auth.login'))
        
    # datetime-local 預設時間格式需要 '%Y-%m-%dT%H:%M'
    now_formatted = datetime.now().strftime('%Y-%m-%dT%H:%M')
    return render_template('logs/new.html', default_time=now_formatted)

@logs_bp.route('/new', methods=['POST'])
def create_log():
    """
    處理新增記錄表單提交。
    
    輸入：
    - request.form['bristol_type'] (int, 1-7)
    - request.form['color']        (str)
    - request.form['odor']         (str, 可選)
    - request.form['mood']         (str)
    - request.form['note']         (str, 可選)
    - request.form['date_time']    (str, 格式通常為 ISO 或是 datetime-local 格式)
    
    業務邏輯：
    1. 驗證登入狀態。
    2. 驗證輸入欄位 (bristol_type 介於 1-7，其他選項需符合系統預定義清單)。
    3. 解析 date_time 字串。
    4. 呼叫 PoopLog.create(bristol_type, color, mood, date_time, user_id, odor, note)。
    5. 成功儲存後，重導向至單次分析結果頁面 '/analysis/<new_log_id>'。
    
    錯誤處理：
    - 若欄位驗證失敗，flash 錯誤訊息並重新渲染 'logs/new.html'，帶回原輸入。
    """
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
        
    bristol_type_str = request.form.get('bristol_type')
    color = request.form.get('color', '').strip()
    odor = request.form.get('odor', '').strip() or None
    mood = request.form.get('mood', '').strip()
    note = request.form.get('note', '').strip() or None
    date_time_str = request.form.get('date_time', '')
    
    # 欄位驗證
    if not bristol_type_str or not color or not mood:
        flash("布里斯托類型、顏色與心情皆為必填欄位！", "error")
        return render_template('logs/new.html', default_time=date_time_str)
        
    try:
        bristol_type = int(bristol_type_str)
        if not (1 <= bristol_type <= 7):
            raise ValueError()
    except ValueError:
        flash("無效的布里斯托大便類型編號，必須為 1 到 7 之間！", "error")
        return render_template('logs/new.html', default_time=date_time_str)
        
    # 解析日期時間
    try:
        date_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        date_time = datetime.utcnow()
        
    try:
        new_log = PoopLog.create(
            bristol_type=bristol_type,
            color=color,
            mood=mood,
            date_time=date_time,
            user_id=user_id,
            odor=odor,
            note=note
        )
        flash("成功建立排便記錄！", "success")
        return redirect(url_for('analysis.view_result', id=new_log.id))
    except Exception as e:
        flash("建立排便記錄時發生錯誤，請稍後再試。", "error")
        return render_template('logs/new.html', default_time=date_time_str)

@logs_bp.route('/<int:id>', methods=['GET'])
def detail_log(id):
    """
    顯示單筆記錄詳細資訊。
    
    輸入：
    - URL 參數 id (記錄 ID)
    
    業務邏輯：
    1. 驗證登入狀態。
    2. 呼叫 PoopLog.get_by_id(id) 查詢該筆記錄。
    3. 若記錄不存在，回傳 404 錯誤。
    4. 檢查權限：若記錄的 user_id 與當前 user_id 不符，回傳 403 拒絕存取。
    5. 渲染 'logs/detail.html' 模板，傳遞該 log 物件。
    """
    user_id = session.get('user_id')
    if not user_id:
        flash("請先登入系統！", "error")
        return redirect(url_for('auth.login'))
        
    log = PoopLog.get_by_id(id)
    if not log:
        flash("該筆日誌紀錄不存在！", "error")
        return render_template('errors/404.html'), 404
        
    if log.user_id != user_id:
        flash("您無權限查看此日誌紀錄！", "error")
        return render_template('errors/403.html'), 403
        
    return render_template('logs/detail.html', log=log)

@logs_bp.route('/<int:id>/edit', methods=['GET'])
def edit_log(id):
    """
    顯示編輯記錄表單。
    
    輸入：
    - URL 參數 id
    
    業務邏輯：
    1. 驗證登入狀態。
    2. 查詢該筆紀錄並驗證擁有權 (user_id)。若非本人紀錄或不存在，回傳 403 或 404。
    3. 渲染 'logs/edit.html'，並預填表單欄位。
    """
    user_id = session.get('user_id')
    if not user_id:
        flash("請先登入系統！", "error")
        return redirect(url_for('auth.login'))
        
    log = PoopLog.get_by_id(id)
    if not log:
        flash("該筆日誌紀錄不存在！", "error")
        return render_template('errors/404.html'), 404
        
    if log.user_id != user_id:
        flash("您無權限編輯此日誌紀錄！", "error")
        return render_template('errors/403.html'), 403
        
    # datetime-local 格式化
    formatted_time = log.date_time.strftime('%Y-%m-%dT%H:%M')
    return render_template('logs/edit.html', log=log, formatted_time=formatted_time)

@logs_bp.route('/<int:id>/edit', methods=['POST'])
def update_log(id):
    """
    處理編輯記錄表單提交 (更新動作)。
    
    輸入：
    - URL 參數 id
    - 表單欄位 bristol_type, color, odor, mood, note, date_time
    
    業務邏輯：
    1. 驗證登入狀態。
    2. 查詢該筆紀錄並驗證擁有權。
    3. 驗證新輸入資料之合法性。
    4. 呼叫 log.update() 更新資料。
    5. 重導向至該紀錄之詳細頁面 '/logs/<id>'。
    """
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
        
    log = PoopLog.get_by_id(id)
    if not log:
        return render_template('errors/404.html'), 404
        
    if log.user_id != user_id:
        return render_template('errors/403.html'), 403
        
    bristol_type_str = request.form.get('bristol_type')
    color = request.form.get('color', '').strip()
    odor = request.form.get('odor', '').strip() or None
    mood = request.form.get('mood', '').strip()
    note = request.form.get('note', '').strip() or None
    date_time_str = request.form.get('date_time', '')
    
    if not bristol_type_str or not color or not mood:
        flash("布里斯托類型、顏色與心情皆為必填欄位！", "error")
        formatted_time = log.date_time.strftime('%Y-%m-%dT%H:%M')
        return render_template('logs/edit.html', log=log, formatted_time=formatted_time)
        
    try:
        bristol_type = int(bristol_type_str)
        if not (1 <= bristol_type <= 7):
            raise ValueError()
    except ValueError:
        flash("無效的布里斯托大便類型編號，必須為 1 到 7 之間！", "error")
        formatted_time = log.date_time.strftime('%Y-%m-%dT%H:%M')
        return render_template('logs/edit.html', log=log, formatted_time=formatted_time)
        
    try:
        date_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        date_time = log.date_time
        
    try:
        log.update(
            bristol_type=bristol_type,
            color=color,
            odor=odor,
            mood=mood,
            note=note,
            date_time=date_time
        )
        flash("成功更新排便記錄！", "success")
        return redirect(url_for('logs.detail_log', id=log.id))
    except Exception as e:
        flash("更新排便記錄時發生錯誤，請稍後再試。", "error")
        formatted_time = log.date_time.strftime('%Y-%m-%dT%H:%M')
        return render_template('logs/edit.html', log=log, formatted_time=formatted_time)

@logs_bp.route('/<int:id>/delete', methods=['POST'])
def delete_log(id):
    """
    處理刪除記錄。
    
    輸入：
    - URL 參數 id
    
    業務邏輯：
    1. 驗證登入狀態。
    2. 查詢該筆紀錄並驗證擁有權。
    3. 呼叫 log.delete() 移除資料。
    4. flash 刪除成功提示。
    5. 重導向至列表頁面 '/logs'。
    """
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
        
    log = PoopLog.get_by_id(id)
    if not log:
        return render_template('errors/404.html'), 404
        
    if log.user_id != user_id:
        return render_template('errors/403.html'), 403
        
    try:
        log.delete()
        flash("排便日誌已順利刪除！", "success")
    except Exception as e:
        flash("刪除排便記錄時發生錯誤。", "error")
        
    return redirect(url_for('logs.list_logs'))
