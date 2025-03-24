import os
import django
import hashlib
from tqdm import tqdm  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from password_checker.models import Password

ROCKYOU_PATH = os.getenv("ROCKYOU_PATH", "data/rockyou.txt")
BATCH_SIZE = 1000  

def hash_password(password):
    """Hash a password using SHA-1."""
    return hashlib.sha1(password.encode('utf-8')).hexdigest()

def run():

    bulk_list = []      
    bulk_hashes = set() 

    with open(ROCKYOU_PATH, 'r', encoding='latin-1') as file:
        for line in tqdm(file, desc="Import progress", unit=" password"):
            password = line.strip()
            hash_value = hash_password(password)

            if hash_value not in bulk_hashes and not Password.objects.filter(hash=hash_value).exists():
                bulk_list.append(Password(hash=hash_value))
                bulk_hashes.add(hash_value)

                if len(bulk_list) >= BATCH_SIZE:
                    try:
                        Password.objects.bulk_create(bulk_list)
                        bulk_list = []
                        bulk_hashes = set()
                    except Exception as e:
                        print(f"Erreur d'insertion en bulk : {e}")

    if bulk_list:
        try:
            Password.objects.bulk_create(bulk_list)
        except Exception as e:
            print(f"Error for bulk insertion : {e}")

    print("Import done successfully !")