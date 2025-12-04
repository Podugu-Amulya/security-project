# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import pyotp
import base64

# Create the FastAPI app instance
app = FastAPI(title="Secure TOTP Microservice")

# --- Schemas ---
class VerifyRequest(BaseModel):
    code: str

# --- Helper to load seed ---
def load_seed_base32():
    """Reads the decrypted seed (hex) and converts it to base32 for TOTP."""
    try:
        # 1. Read the 64-character hex seed from the mounted volume
        with open("/app/data/seed.txt", "r") as f:
            hex_seed = f.read().strip()
            
        if len(hex_seed) != 64:
             return None

        # 2. Convert hex seed bytes to base32 (standard for pyotp)
        hex_bytes = bytes.fromhex(hex_seed)
        base32_seed = base64.b32encode(hex_bytes).decode().rstrip('=')
        
        return base32_seed
        
    except FileNotFoundError:
        return None
    except Exception:
        return None

# --- API Endpoints ---

@app.post("/generate-2fa")
def post_generate_2fa():
    """Generates the current TOTP code using the stored seed."""
    base32_seed = load_seed_base32()
    
    if not base32_seed:
        raise HTTPException(
            status_code=500,
            detail={"status": "fail", "code": "Seed not found or invalid."}
        )
    
    # TOTP settings: SHA1, 6 digits, 30 seconds (default pyotp)
    totp = pyotp.TOTP(base32_seed)
    current_code = totp.now()

    return {"status": "ok", "code": current_code}


@app.post("/verify-2fa")
def post_verify_2fa(request: VerifyRequest):
    """Verifies a provided TOTP code against the stored seed."""
    base32_seed = load_seed_base32()
    
    if not base32_seed:
        raise HTTPException(
            status_code=500,
            detail={"status": "fail", "code": "Seed not found or invalid."}
        )

    totp = pyotp.TOTP(base32_seed)
    
    # Verify the code (checks time windows +/- 1 period)
    is_valid = totp.verify(request.code, valid_window=1) 
    
    return {"status": "ok", "valid": is_valid}