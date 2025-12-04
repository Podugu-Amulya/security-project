# app/cron_job.py

import os
import sys
import datetime
import pyotp
import base64

# --- Configuration ---
SEED_PATH = "/app/data/seed.txt"
LOG_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# --- TOTP Generation Logic ---
def load_seed_base32():
    """Reads the decrypted seed (hex) and converts it to base32 for TOTP."""
    try:
        with open(SEED_PATH, 'r') as f:
            hex_seed = f.read().strip()
            
        if len(hex_seed) != 64:
             return None
             
        # Convert hex seed bytes to base32
        hex_bytes = bytes.fromhex(hex_seed)
        base32_seed = base64.b32encode(hex_bytes).decode().rstrip('=')
        
        return base32_seed
        
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"ERROR: Failed to load or process seed: {e}", file=sys.stderr)
        return None

def generate_totp(base32_seed):
    """Generates the current 6-digit TOTP code."""
    totp = pyotp.TOTP(base32_seed)
    return totp.now()

# --- Cron Main Logic ---
def run_cron_job():
    """Reads seed, generates TOTP, and logs the output every minute."""
    base32_seed = load_seed_base32()
    
    if not base32_seed:
        timestamp = datetime.datetime.now().strftime(LOG_TIME_FORMAT)
        print(f"[{timestamp} ZFA CODE: XXXXXX] ERROR: Seed not found or invalid at {SEED_PATH}.", file=sys.stderr)
        return

    current_totp_code = generate_totp(base32_seed)

    timestamp = datetime.datetime.now().strftime(LOG_TIME_FORMAT)
    log_message = f"{timestamp} - ZFA CODE: {current_totp_code}"
    
    print(log_message)


if __name__ == "__main__":
    run_cron_job()