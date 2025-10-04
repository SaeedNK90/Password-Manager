from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())
print("\nOn your system, place this value in the FERNET_KEY environment variable (e.g. in .env or CI/CD).")
