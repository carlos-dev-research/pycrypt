import os
import argparse
import shutil
import zipfile
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
from getpass import getpass

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_file(file_path, password):
    # Generate a salt
    salt = os.urandom(16)
    
    # Derive the key from the password and salt
    key = derive_key(password, salt)
    
    # Initialize Fernet with the key
    fernet = Fernet(key)
    
    # Encrypt the file
    with open(file_path, 'rb') as file:
        original_file = file.read()
    
    encrypted_file = fernet.encrypt(original_file)
    
    # Save the salt and the encrypted file with a new name
    encrypted_file_path = file_path + '.encrypted'
    with open(encrypted_file_path, 'wb') as file:
        file.write(salt + encrypted_file)
    

def decrypt_file(file_path, password):
    # Read the salt and encrypted file
    with open(file_path, 'rb') as file:
        salt = file.read(16)  # The first 16 bytes are the salt
        encrypted_file = file.read()
    
    # Derive the key from the password and salt
    key = derive_key(password, salt)
    
    # Initialize Fernet with the key
    fernet = Fernet(key)
    
    # Decrypt the file
    decrypted_file = fernet.decrypt(encrypted_file)
    
    # Save the decrypted file with a new name
    decrypted_file_path = file_path.replace('.encrypted', '')
    with open(decrypted_file_path, 'wb') as file:
        file.write(decrypted_file)
    
    # If the decrypted file is a zip file, extract it and remove the zip
    if decrypted_file_path.endswith('.zip'):
        output_folder_path = decrypted_file_path.replace('.zip', '')
        decompress_folder(decrypted_file_path, output_folder_path)
        os.remove(decrypted_file_path)

def compress_folder(folder_path, output_path):
    shutil.make_archive(output_path, 'zip', folder_path)

def decompress_folder(zip_path, output_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_path)

def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt files and folders.")
    parser.add_argument("action", choices=["encrypt", "decrypt"], help="Action to perform: encrypt or decrypt.")
    parser.add_argument("path", help="Path to the file or folder to process.")
    
    args = parser.parse_args()
    
    password = getpass("Enter the password: ")
    
    if args.action == "encrypt":
        if os.path.isdir(args.path):
            # Compress the folder
            zip_path = args.path + '.zip'
            compress_folder(args.path, args.path)
            # Encrypt the zip file
            encrypt_file(zip_path, password)
            # Optionally delete the original folder after encryption
            os.remove(zip_path)

        elif os.path.isfile(args.path):
            encrypt_file(args.path, password)
    
    elif args.action == "decrypt":
        if os.path.isfile(args.path) and args.path.endswith('.encrypted'):
            # Decrypt the file
            decrypt_file(args.path, password)

if __name__ == "__main__":
    main()

