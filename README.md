# 🔐 Password Manager

A secure and simple password manager built with Flask.  
Store, encrypt, and manage your passwords safely with user authentication, CSRF protection, and encrypted storage.

## 🚀 Features
- User registration & login (with hashed passwords)
- Add, view, and manage saved passwords
- Strong encryption using Fernet (stored securely)
- CSRF protection with Flask-WTF
- SQLAlchemy ORM support (SQLite by default, can be switched to PostgreSQL/MySQL)
- Ready for deployment (Docker/Production)

## 🛠 Installation

### 1. Clone the repository
```bash
git clone https://github.com/SaeedNK90/Password-Manager.git
cd password-manager
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate    # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set environment variables
Create a `.env` file in the root folder:
```
SECRET_KEY=your-very-strong-secret-key
FERNET_KEY=your-generated-fernet-key
SQLALCHEMY_DATABASE_URI=sqlite:///app.db
```

Generate keys (example in Python REPL):
```python
import secrets, cryptography.fernet
print(secrets.token_hex(32))  # SECRET_KEY
print(cryptography.fernet.Fernet.generate_key().decode())  # FERNET_KEY
```

### 5. Initialize the database
```bash
python init_db.py
```

### 6. Run the server
```bash
python run.py
```

Go to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 📦 Deployment
- Use **gunicorn** or **uwsgi** for production
- Serve with **nginx** + **HTTPS**
- Dockerfile is available for containerized deployment

## 🔒 Security Notes
- Never hardcode keys inside the codebase
- Always use HTTPS in production
- Use PostgreSQL/MySQL instead of SQLite for production
- Enable rate limiting on login endpoints
- Never log sensitive data (passwords, encryption keys)

## 📜 License
MIT License
