# 資料庫設計文件 (DB DESIGN)

**專案名稱：** 糞便日誌 (Poop Journal)  
**版本：** v1.0  
**建立日期：** 2026-05-26  
**資料庫類型：** SQLite  
**ORM 框架：** Flask-SQLAlchemy (SQLAlchemy 2.x)

---

## 1. 實體關係圖 (ER Diagram)

以下是系統的實體關係圖，包含 `users` (使用者)、`poop_logs` (排便記錄) 與 `diet_suggestions` (飲食建議)。

```mermaid
erDiagram
    users ||--o{ poop_logs : "has"
    users ||--o{ diet_suggestions : "receives"

    users {
        int id PK "INTEGER PRIMARY KEY AUTOINCREMENT"
        string username UNIQUE "VARCHAR(80) UNIQUE, NOT NULL"
        string password_hash "VARCHAR(255) NOT NULL"
        datetime created_at "DATETIME, DEFAULT CURRENT_TIMESTAMP"
    }

    poop_logs {
        int id PK "INTEGER PRIMARY KEY AUTOINCREMENT"
        int user_id FK "INTEGER, NULLABLE"
        int bristol_type "INTEGER CHECK(1-7), NOT NULL"
        string color "VARCHAR(30), NOT NULL"
        string odor "VARCHAR(30), NULLABLE"
        string mood "VARCHAR(30), NOT NULL"
        string note "TEXT, NULLABLE"
        datetime date_time "DATETIME, NOT NULL"
        datetime created_at "DATETIME, DEFAULT CURRENT_TIMESTAMP"
        datetime updated_at "DATETIME, DEFAULT CURRENT_TIMESTAMP"
    }

    diet_suggestions {
        int id PK "INTEGER PRIMARY KEY AUTOINCREMENT"
        int user_id FK "INTEGER, NOT NULL"
        string summary "VARCHAR(100), NOT NULL"
        string content "TEXT, NOT NULL"
        datetime created_at "DATETIME, DEFAULT CURRENT_TIMESTAMP"
    }
```

---

## 2. 資料表詳細說明

### 2.1 `users` (使用者帳號表)
- **用途**：記錄使用者基本資訊與登入憑證。
- **欄位列表**：

| 欄位名稱 | 資料型別 | 屬性 / 約束 | 說明 |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | 使用者唯一識別碼 |
| `username` | VARCHAR(80) | UNIQUE, NOT NULL | 使用者帳號（不可重覆） |
| `password_hash` | VARCHAR(255) | NOT NULL | 經 Hash 加密後之密碼 |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | 帳號建立時間 |

### 2.2 `poop_logs` (排便記錄表)
- **用途**：記錄使用者的每一筆排便資訊。
- **欄位列表**：

| 欄位名稱 | 資料型別 | 屬性 / 約束 | 說明 |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | 排便記錄唯一識別碼 |
| `user_id` | INTEGER | FOREIGN KEY (`users.id`), NULLABLE | 所屬使用者 ID (可為 Null 支援訪客模式) |
| `bristol_type` | INTEGER | CHECK (1-7), NOT NULL | 布里斯托大便分類類型 (1 至 7) |
| `color` | VARCHAR(30) | NOT NULL | 糞便顏色 (例如: brown, green, yellow...) |
| `odor` | VARCHAR(30) | NULLABLE | 糞便氣味 (例如: normal, smelly, very_smelly...) |
| `mood` | VARCHAR(30) | NOT NULL | 填寫紀錄時的心情 (例如: happy, anxious, normal...) |
| `note` | TEXT | NULLABLE | 備註與額外補充說明 |
| `date_time` | DATETIME | NOT NULL | 實際排便日期與時間 |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | 資料建立時間 |
| `updated_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | 資料最後更新時間 |

### 2.3 `diet_suggestions` (飲食建議快取表)
- **用途**：儲存系統或 AI 針對使用者近期狀況產出的飲食與健康建議。
- **欄位列表**：

| 欄位名稱 | 資料型別 | 屬性 / 約束 | 說明 |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | 建議記錄唯一識別碼 |
| `user_id` | INTEGER | FOREIGN KEY (`users.id`), NOT NULL | 對應之使用者 ID |
| `summary` | VARCHAR(100) | NOT NULL | 建議之摘要 (例如: 便秘警告、理想狀態、水分不足等) |
| `content` | TEXT | NOT NULL | 詳細建議內容 (例如 markdown 或 JSON 格式字串) |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | 建議產出時間 |

---

## 3. SQL 建表語法 (SQLite)

完整的 DDL 定義檔案位於 [schema.sql](file:///c:/Users/User/Downloads/pooppoop/database/schema.sql)：

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS poop_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    bristol_type INTEGER NOT NULL CHECK (bristol_type BETWEEN 1 AND 7),
    color VARCHAR(30) NOT NULL,
    odor VARCHAR(30),
    mood VARCHAR(30) NOT NULL,
    note TEXT,
    date_time DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS diet_suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    summary VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

## 4. Python Model 程式碼與 CRUD 實作

所有 Model 以 **Flask-SQLAlchemy** 定義，並在類別內封裝標準的 CRUD 介面。

### 4.1 初始化與匯出入口 `app/models/__init__.py`
位於 [__init__.py](file:///c:/Users/User/Downloads/pooppoop/app/models/__init__.py)：
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 延遲相對導入，避免循環參照
from .user import User
from .log import PoopLog
from .suggestion import DietSuggestion

__all__ = ['db', 'User', 'PoopLog', 'DietSuggestion']
```

### 4.2 `User` Model
位於 [user.py](file:///c:/Users/User/Downloads/pooppoop/app/models/user.py)：
```python
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯設定
    poop_logs = db.relationship('PoopLog', backref='user', lazy=True, cascade="all, delete-orphan")
    diet_suggestions = db.relationship('DietSuggestion', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # --- CRUD Methods ---
    @classmethod
    def create(cls, username, password):
        user = cls(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def update(self, username=None, password=None):
        if username:
            self.username = username
        if password:
            self.set_password(password)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
```

### 4.3 `PoopLog` Model
位於 [log.py](file:///c:/Users/User/Downloads/pooppoop/app/models/log.py)：
```python
from datetime import datetime
from app.models import db

class PoopLog(db.Model):
    __tablename__ = 'poop_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    bristol_type = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(30), nullable=False)
    odor = db.Column(db.String(30), nullable=True)
    mood = db.Column(db.String(30), nullable=False)
    note = db.Column(db.Text, nullable=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- CRUD Methods ---
    @classmethod
    def create(cls, bristol_type, color, mood, date_time, user_id=None, odor=None, note=None):
        log = cls(
            user_id=user_id,
            bristol_type=bristol_type,
            color=color,
            odor=odor,
            mood=mood,
            note=note,
            date_time=date_time
        )
        db.session.add(log)
        db.session.commit()
        return log

    @classmethod
    def get_by_id(cls, log_id):
        return cls.query.get(log_id)

    @classmethod
    def get_all(cls, user_id=None, start_date=None, end_date=None):
        query = cls.query
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        if start_date:
            query = query.filter(cls.date_time >= start_date)
        if end_date:
            query = query.filter(cls.date_time <= end_date)
        # 預設按排便時間降序排列
        return query.order_by(cls.date_time.desc()).all()

    def update(self, bristol_type=None, color=None, odor=None, mood=None, note=None, date_time=None):
        if bristol_type is not None:
            self.bristol_type = bristol_type
        if color is not None:
            self.color = color
        if odor is not None:
            self.odor = odor
        if mood is not None:
            self.mood = mood
        if note is not None:
            self.note = note
        if date_time is not None:
            self.date_time = date_time
        
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
```

### 4.4 `DietSuggestion` Model
位於 [suggestion.py](file:///c:/Users/User/Downloads/pooppoop/app/models/suggestion.py)：
```python
from datetime import datetime
from app.models import db

class DietSuggestion(db.Model):
    __tablename__ = 'diet_suggestions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    summary = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # --- CRUD Methods ---
    @classmethod
    def create(cls, user_id, summary, content):
        suggestion = cls(user_id=user_id, summary=summary, content=content)
        db.session.add(suggestion)
        db.session.commit()
        return suggestion

    @classmethod
    def get_by_id(cls, suggestion_id):
        return cls.query.get(suggestion_id)

    @classmethod
    def get_by_user_id(cls, user_id, limit=10):
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).limit(limit).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
```
