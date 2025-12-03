from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generate the Private Key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
)

# Save Private Key (student_private.pem)
with open("student_private.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Generate and Save Public Key (student_public.pem)
public_key = private_key.public_key()
with open("student_public.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print("Keys created successfully! Look for .pem files in your folder.")