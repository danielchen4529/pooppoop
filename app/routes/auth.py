from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET'])
def register():
    """
    顯示註冊頁面。
    
    業務邏輯：
    - 若 session 中已有 user_id (已登入)，重導向至首頁 '/'。
    - 否則，渲染 'auth/register.html'。
    """
    pass

@auth_bp.route('/register', methods=['POST'])
def register_post():
    """
    處理註冊表單提交。
    
    輸入：
    - request.form['username']
    - request.form['password']
    - request.form['confirm_password']
    
    業務邏輯：
    1. 驗證所有欄位是否填寫。
    2. 驗證 password 與 confirm_password 是否一致且長度符合安全要求。
    3. 呼叫 User.get_by_username() 檢查該帳號是否已被註冊。
    4. 若通過驗證，呼叫 User.create() 新增使用者。
    5. 將新建立的 user.id 存入 session['user_id'] 進行自動登入。
    6. 重導向至首頁 '/'，並 flash 成功註冊訊息。
    
    錯誤處理：
    - 驗證失敗時，使用 flash() 傳遞錯誤原因，並回傳渲染 'auth/register.html'，可帶回原填寫的 username。
    """
    pass

@auth_bp.route('/login', methods=['GET'])
def login():
    """
    顯示登入頁面。
    
    業務邏輯：
    - 若已登入，重導向至首頁 '/'。
    - 否則，渲染 'auth/login.html'。
    """
    pass

@auth_bp.route('/login', methods=['POST'])
def login_post():
    """
    處理登入表單提交。
    
    輸入：
    - request.form['username']
    - request.form['password']
    
    業務邏輯：
    1. 驗證欄位是否填寫。
    2. 呼叫 User.get_by_username() 查詢該使用者。
    3. 若使用者存在，且呼叫 user.check_password() 驗證密碼成功：
       - 將 user.id 存入 session['user_id']。
       - 重導向至首頁 '/'。
    4. 若驗證失敗，flash 錯誤訊息並重新渲染登入頁面。
    """
    pass

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    處理登出動作。
    
    業務邏輯：
    - 清除 session['user_id'] (可清除整個 session)。
    - flash 登出成功提示。
    - 重導向至登入頁面 '/login'。
    """
    pass
