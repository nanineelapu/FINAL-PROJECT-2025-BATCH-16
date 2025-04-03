import os
import pickle
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from ecies import encrypt, decrypt
from ecies.utils import generate_eth_key

# CP-ABE Functions (Using ECIES as a placeholder for CP-ABE)
def CPABE_generate_keys():
    """
    Generates and stores public/private keys if they don't exist.
    Returns (private_key, public_key) as hex strings.
    """
    key_dir = "CyberSecurityApp/static/public"
    if not os.path.exists(key_dir):
        os.makedirs(key_dir, exist_ok=True)
    pub_path = "CyberSecurityApp/static/public/key.pub"
    priv_path = "CyberSecurityApp/static/public/key.priv"
    if not os.path.exists(pub_path) or not os.path.exists(priv_path):
        secret_key = generate_eth_key()
        private_key = secret_key.to_hex()
        public_key = secret_key.public_key.to_hex()
        with open(pub_path, 'wb') as f:
            pickle.dump(public_key, f)
        with open(priv_path, 'wb') as f:
            pickle.dump(private_key, f)
    else:
        with open(pub_path, 'rb') as f:
            public_key = pickle.load(f)
        with open(priv_path, 'rb') as f:
            private_key = pickle.load(f)
    return private_key, public_key

def CPABE_encrypt(data, public_key):
    """
    Encrypts data using CP-ABE (here via ECIES encrypt as a placeholder).
    """
    return encrypt(public_key, data)

def CPABE_decrypt(encrypted_data, private_key):
    """
    Decrypts data using CP-ABE (via ECIES decrypt as a placeholder).
    """
    return decrypt(private_key, encrypted_data)

# AES Functions
def aes_encrypt(data, symmetric_key):
    cipher = AES.new(symmetric_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return {"nonce": cipher.nonce, "ciphertext": ciphertext, "tag": tag}

def aes_decrypt(enc_data, symmetric_key):
    cipher = AES.new(symmetric_key, AES.MODE_EAX, nonce=enc_data["nonce"])
    return cipher.decrypt_and_verify(enc_data["ciphertext"], enc_data["tag"])

# Hybrid Encryption Functions
def hybrid_encrypt_file(file_data, access_policy, public_key):
    """
    Hybrid encryption:
      1. Generate a random AES key.
      2. Encrypt file_data using AES.
      3. Encrypt the AES key using CP-ABE.
      4. Return a package containing both encrypted parts.
    (The access_policy parameter is a placeholder to illustrate where you would
    enforce an access policy in a full CP-ABE system.)
    """
    symmetric_key = get_random_bytes(16)  # 128-bit AES key
    aes_encrypted = aes_encrypt(file_data, symmetric_key)
    # Encrypt the AES key (convert to hex string bytes)
    symmetric_key_hex = symmetric_key.hex().encode()
    encrypted_symmetric_key = CPABE_encrypt(symmetric_key_hex, public_key)
    return {"aes_encrypted": aes_encrypted, "encrypted_symmetric_key": encrypted_symmetric_key}

def hybrid_decrypt_file(package, private_key):
    """
    Hybrid decryption:
      1. Decrypt the AES key using CP-ABE.
      2. Use the AES key to decrypt the file data.
    """
    encrypted_symmetric_key = package["encrypted_symmetric_key"]
    symmetric_key_hex = CPABE_decrypt(encrypted_symmetric_key, private_key)
    symmetric_key = bytes.fromhex(symmetric_key_hex.decode())
    file_data = aes_decrypt(package["aes_encrypted"], symmetric_key)
    return file_data
