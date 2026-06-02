from flask import Blueprint, render_template, request, redirect, url_for, session, flash

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/', methods=['GET'])
def list_logs():
    """
    歷史記錄列表。
    
    輸入：
    - request.args.get('start_date')  (格式: 'YYYY-MM-DD', 可選)
    - request.args.get('end_date')    (格式: 'YYYY-MM-DD', 可選)
    
    業務邏輯：
    1. 驗證登入狀態 (檢查 session['user_id'])。若未登入，重導向至 '/login'。
    2. 解析 start_date 與 end_date 字串為 datetime.date 物件。
    3. 呼叫 PoopLog.get_all(user_id=current_user, start_date=..., end_date=...) 查詢記錄列表。
    4. 將紀錄清單渲染至 'logs/list.html' 模板。
    """
    pass

@logs_bp.route('/new', methods=['GET'])
def new_log():
    """
    顯示新增記錄表單頁面。
    
    業務邏輯：
    - 驗證登入狀態。
    - 渲染 'logs/new.html' 模板。預設時間設為當前時間。
    """
    pass

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
    pass

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
    pass

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
    pass

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
    pass

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
    pass
