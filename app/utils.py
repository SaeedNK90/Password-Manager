import os
from cryptography.fernet import Fernet


def _load_key():
    key = os.environ.get('FERNET_KEY')
    if key:
        return key.encode() if isinstance(key, str) else key
    generated = Fernet.generate_key()
    print("WARNING: No FERNET_KEY found in environment. Using a generated key (not persistent).")
    print("Run 'python generate_fernet_key.py' and set FERNET_KEY env var for production.")
    return generated


_KEY = _load_key()
_CIPHER = Fernet(_KEY)


def encrypt_password(password: str) -> str:
    token = _CIPHER.encrypt(password.encode())
    return token.decode()


def decrypt_password(token: str) -> str:
    return _CIPHER.decrypt(token.encode()).decode()
