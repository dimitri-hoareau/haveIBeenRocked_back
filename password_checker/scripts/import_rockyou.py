import os
import django
import hashlib
from django.conf import settings
from tqdm import tqdm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from password_checker.models import Password

ROCKYOU_PATH = os.getenv("ROCKYOU_PATH", "data/rockyou.txt")

def hash_password(password):
    return hashlib.sha1(password.encode('utf-8')).hexdigest()

def run():
    with open(ROCKYOU_PATH, 'r', encoding='latin-1') as file:
        for line in tqdm(file, desc="Import progress", unit=" password"):
            password = line.strip()
            hash_value = hash_password(password)

            if not Password.objects.filter(hash=hash_value).exists():
                try:
                    Password.objects.create(hash=hash_value)
                except Exception as e:
                    print(f"Error for {hash_value} : {e}")

    print("Import done successfully !")
