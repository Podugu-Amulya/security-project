from flask import Flask, request, jsonify
import pyotp
import os

app = Flask(__name__)
# Persistence path
SEED_FILE = "data/seed.txt"

@app.route('/decrypt-seed', methods=['POST'])
def decrypt_seed():
    data = request.json
    encrypted_seed = data.get("encrypted_seed")
    # Add your specific decryption logic here 
    # For now, we save the seed to the persistent file
    with open(SEED_FILE, "w") as f:
        f.write(encrypted_seed) 
    return jsonify({"status": "success", "message": "Seed stored"}), 200

@app.route('/generate-2fa', methods=['GET'])
def generate_2fa():
    if not os.path.exists(SEED_FILE):
        return jsonify({"error": "No seed found"}), 400
    with open(SEED_FILE, "r") as f:
        seed = f.read()
    totp = pyotp.TOTP(seed)
    return jsonify({"code": totp.now()}), 200

@app.route('/verify-2fa', methods=['POST'])
def verify_2fa():
    data = request.json
    user_code = data.get("code")
    with open(SEED_FILE, "r") as f:
        seed = f.read()
    totp = pyotp.TOTP(seed)
    if totp.verify(user_code):
        return jsonify({"status": "valid"}), 200
    return jsonify({"status": "invalid"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)