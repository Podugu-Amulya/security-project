#!/usr/bin/env python3
# Script executed by cron every minute to log the current 2FA code.

import os
from datetime import datetime
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
import pyotp

# --- FILE PATHS ---
# Seed file location (mounted volume)
ENCRYPTED_SEED_PATH = "/app/data/seed.txt"
# Private key location (mounted volume)
PRIVATE_KEY_PATH = "/app/student_private.pem"

# --- 1. DECRYPT SEED ---
def decrypt_seed(encrypted_seed_b64, private_key_path):
    """Reads keys and decrypts the seed using the student's private key."""
    try:
        # Load the student's private key
        with open(private_key_path, "rb") as key_file:
            private_key = load_pem_private_key(key_file.read(), password=None, backend=default_backend())
        
        encrypted_seed = base64.b64decode(encrypted_seed_b64)
        
        # Decrypt using RSA/OAEP with MGF1 and SHA-256 (as required by documentation)
        decrypted_seed = private_key.decrypt(
            encrypted_seed,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        # The result is the Base32-encoded TOTP key
        return decrypted_seed.decode('utf-8')
    except Exception as e:
        # CRITICAL: Log errors to cron output for debugging
        print(f"[{datetime.utcnow().isoformat()}] ERROR during seed decryption: {e}")
        return None

# --- 2. GENERATE AND LOG CODE ---
if __name__ == "__main__":
    try:
        # Read the encrypted seed from the persistent data volume
        with open(ENCRYPTED_SEED_PATH, 'r') as f:
            encrypted_seed_b64 = f.read().strip()
            
        # Decrypt the seed
        totp_key = decrypt_seed(encrypted_seed_b64, PRIVATE_KEY_PATH)
        
        if totp_key:
            # Generate the current TOTP code using the Base32 key
            totp = pyotp.TOTP(totp_key)
            current_code = totp.now()
            
            # Format timestamp using UTC (CRITICAL for verification)
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            
            # Output the required format "[Timestamp] 2FA Code: [Code]" to stdout
            print(f"[{timestamp}] 2FA Code: {current_code}")

    except FileNotFoundError as e:
        print(f"[{datetime.utcnow().isoformat()}] ERROR: Required file not found: {e.filename}. Check volume mounting.")
    except Exception as e:
        print(f"[{datetime.utcnow().isoformat()}] FATAL ERROR in cron job: {e}")