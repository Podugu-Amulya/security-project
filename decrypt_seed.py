from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64
import os
import sys

# --- File Paths ---
ENCRYPTED_SEED_FILE = "encrypted_seed.txt"
PRIVATE_KEY_FILE = "student_private.pem"
DECRYPTED_SEED_PATH = "./data/seed.txt" # Final required location for the microservice

# --- Helper Functions ---

def load_private_key(file_path: str):
    """Loads the student's private key from a PEM file."""
    try:
        with open(file_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None # Keys were generated without password
            )
        return private_key
    except FileNotFoundError:
        print(f"Error: Private key file not found at {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading private key: {e}")
        sys.exit(1)


def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypts the Base64-encoded encrypted seed using RSA/OAEP with SHA-256.
    Returns the 64-character hexadecimal seed.
    """
    # 1. Base64 decode the encrypted seed string
    try:
        encrypted_bytes = base64.b64decode(encrypted_seed_b64)
    except Exception:
        raise ValueError("Failed to Base64 decode the ciphertext.")

    # 2. RSA/OAEP decrypt with SHA-256
    decryptor_padding = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()), # MGF1 with SHA-256
        algorithm=hashes.SHA256(),                   # Hash Algorithm SHA-256
        label=None                                   # Label None
    )

    try:
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            decryptor_padding
        )
    except Exception as e:
        # Common error if key/padding/hash parameters are mismatched
        raise RuntimeError(f"Decryption failed: {e}. Check key and padding parameters.")

    # 3. Decode bytes to UTF-8 string
    decrypted_hex_seed = decrypted_bytes.decode('utf-8')
    
    # 4. Validate that the seed is a 64-character hex string
    if len(decrypted_hex_seed) != 64:
        raise ValueError(f"Decrypted seed length is incorrect: {len(decrypted_hex_seed)}. Expected 64.")
    if not all(c in '0123456789abcdef' for c in decrypted_hex_seed.lower()):
        raise ValueError("Decrypted seed contains non-hexadecimal characters.")

    # 5. Return hex seed
    return decrypted_hex_seed


def run_decryption():
    """Main function to orchestrate loading files, decryption, and saving."""
    
    # 1. Load the required keys and ciphertext
    print("Loading private key and encrypted seed...")
    private_key = load_private_key(PRIVATE_KEY_FILE)
    
    try:
        with open(ENCRYPTED_SEED_FILE, "r") as f:
            encrypted_seed_b64 = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Encrypted seed file not found at {ENCRYPTED_SEED_FILE}.")
        sys.exit(1)

    # 2. Perform Decryption
    print("Decrypting seed...")
    try:
        hex_seed = decrypt_seed(encrypted_seed_b64, private_key)
    except (ValueError, RuntimeError) as e:
        print(f"Decryption Error: {e}")
        sys.exit(1)

    # 3. Save the decrypted seed to the required location for the microservice
    # NOTE: We create the 'data' directory here, but it will be a Docker volume later.
    os.makedirs(os.path.dirname(DECRYPTED_SEED_PATH), exist_ok=True)
    with open(DECRYPTED_SEED_PATH, "w") as f:
        f.write(hex_seed)
        
    print("\nSUCCESS!")
    print(f"Decrypted 64-character seed: {hex_seed}")
    print(f"Seed successfully saved to: {DECRYPTED_SEED_PATH}")
    print("You are ready to implement the FastAPI service and Dockerfile.")


if __name__ == "__main__":
    run_decryption() 