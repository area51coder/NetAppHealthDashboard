from pathlib import Path
from cryptography.fernet import Fernet

CONFIG_DIR = Path("config")
CONFIG_DIR.mkdir(exist_ok=True)

key = Fernet.generate_key()

with open(CONFIG_DIR / "secret.key", "wb") as f:
    f.write(key)

print("Encryption key created successfully.")

key = load_key()

print(key)
print(len(key))

cipher = Fernet(key)