import base64
import hashlib
import os

def generate_pkce():
    # Генерация случайного code_verifier
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).rstrip(b'=').decode('utf-8')

    # Генерация code_challenge на основе code_verifier
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).rstrip(b'=').decode('utf-8')

    print("Code Verifier:", code_verifier)
    print("Code Challenge:", code_challenge)

if __name__ == "__main__":
    generate_pkce()
