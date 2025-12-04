# import requests
# import json
# import os
# import sys

# # --- CONFIGURATION ---
# STUDENT_ID = "23A91A05C0"
# GITHUB_REPO_URL = "https://github.com/Podugu-Amulya/security-project.git"
# # CRITICAL: Verify this URL against your original instructions for any typos.
# API_URL = "https://eajayq4r3djoq4rpovy2nhtdo0vj6fllambda-url.op-south-1.on.aws"

# def get_formatted_public_key(file_path="student_public.pem"):
#     """Reads the public key and formats it as a single line with \n characters."""
#     try:
#         with open(file_path, "r") as f:
#             # Read all lines, strip leading/trailing whitespace from each line
#             lines = [line.strip() for line in f.readlines()]
#             # Join lines with \n, as required by the API
#             key_data = "\\n".join(lines)
#             return key_data
#     except FileNotFoundError:
#         print(f"Error: Public key file not found at {file_path}. Ensure it is in the same folder.")
#         sys.exit(1)

# def request_encrypted_seed():
#     # 1. Read and format the public key
#     public_key = get_formatted_public_key()
#     if not public_key:
#         return

#     # 2. Prepare the HTTP POST payload
#     payload = {
#         "student_id": STUDENT_ID,
#         "github_repo_url": GITHUB_REPO_URL, # Corrected case
#         "public_key": public_key
#     }

#     # 3. Send POST request to Instructor API
#     print(f"Requesting encrypted seed from {API_URL}...")
#     try:
#         response = requests.post(
#             API_URL,
#             json=payload,
#             headers={"Content-Type": "application/json"},
#             timeout=10 # Include timeout handling
#         )
#         response.raise_for_status() 

#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred during the API request: {e}")
#         print("\n!!! DIAGNOSTIC NOTE: The 'Failed to resolve' error usually means the API_URL is down or incorrect. Please contact your instructor. !!!")
#         return

#     # 4. Parse JSON response
#     try:
#         response_data = response.json()
#     except json.JSONDecodeError:
#         print(f"Error: Could not decode JSON response. Status code: {response.status_code}")
#         print(f"Response text: {response.text[:100]}...")
#         return

#     # 5. Extract 'encrypted_seed' field and handle success/failure
#     if response_data.get("status") == "success" and "encrypted_seed" in response_data:
#         encrypted_seed = response_data["encrypted_seed"]
        
#         # 6. Save the encrypted seed to file (encrypted_seed.txt as plain text)
#         output_file = "encrypted_seed.txt"
#         with open(output_file, "w") as f:
#             f.write(encrypted_seed)
        
#         print("\nSUCCESS!")
#         print(f"Encrypted seed received and saved to: {output_file}")
#         print("IMPORTANT: DO NOT commit this 'encrypted_seed.txt' file to Git.")
#     else:
#         print(f"\nAPI Error Response: {response_data.get('error', 'Unknown error.')}")
#         print("Please check your student ID, repo URL, and public key formatting.")

# if __name__ == "__main__":
#     request_encrypted_seed()



# import requests

# def request_seed(student_id: str, github_repo_url: str, api_url: str):
#     """
#     Request encrypted seed from instructor API
#     """

#     # 1. Read student public key
#     with open("student_public.pem", "r") as f:
#         public_key = f.read()  # keep BEGIN/END lines

#     # 2. Prepare payload
#     payload = {
#         "student_id": student_id,
#         "github_repo_url": github_repo_url,
#         "public_key": public_key
#     }

#     # 3. Send POST request
#     try:
#         response = requests.post(api_url, json=payload, timeout=10)
#         response.raise_for_status()
#     except requests.RequestException as e:
#         print("HTTP Request failed:", e)
#         return

#     # 4. Parse JSON response
#     data = response.json()
#     if data.get("status") == "success":
#         encrypted_seed = data["encrypted_seed"]

#         # 5. Save encrypted seed
#         with open("encrypted_seed.txt", "w") as f:
#             f.write(encrypted_seed)
#         print("Encrypted seed saved to encrypted_seed.txt")
#     else:
#         print("Error from API:", data)



# if _name_ == "_main_": 
#     student_id = input("Enter your Student ID: ").strip()
#     github_repo_url = input("Enter your GitHub Repo URL: ").strip()

#     api_url = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

#     request_seed(student_id, github_repo_url, api_url)






import requests

def request_seed(student_id: str, github_repo_url: str, api_url: str):
    """
    Request encrypted seed from instructor API
    """

    # 1. Read student public key
    with open("student_public.pem", "r") as f:
        public_key = f.read()  # keep BEGIN/END lines

    # 2. Prepare payload
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key
    }

    # 3. Send POST request
    try:
        response = requests.post(api_url, json=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("HTTP Request failed:", e)
        return

    # 4. Parse JSON response
    data = response.json()
    if data.get("status") == "success":
        encrypted_seed = data["encrypted_seed"]

        # 5. Save encrypted seed
        with open("encrypted_seed.txt", "w") as f:
            f.write(encrypted_seed)
        print("Encrypted seed saved to encrypted_seed.txt")
    else:
        print("Error from API:", data)



if __name__== "__main__":

    student_id = input("Enter your Student ID: ").strip()
    github_repo_url = input("Enter your GitHub Repo URL: ").strip()

    api_url = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

    request_seed(student_id, github_repo_url, api_url)
