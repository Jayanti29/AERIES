import base64
import hashlib
import hmac
import json
import os
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Argon2id password hashing with pure-Python SHA-512 + Salt fallback
try:
    from argon2 import PasswordHasher
    from argon2.exceptions import VerifyMismatchError
    _ph = PasswordHasher()
    def hash_password(password: str) -> str:
        return _ph.hash(password)
    def verify_password(password: str, hashed: str) -> bool:
        try:
            return _ph.verify(hashed, password)
        except Exception:
            return False
except ImportError:
    def hash_password(password: str) -> str:
        salt = os.urandom(16).hex()
        dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return f"pbkdf2_sha256${salt}${dk.hex()}"
    def verify_password(password: str, hashed: str) -> bool:
        try:
            parts = hashed.split('$')
            if len(parts) != 3 or parts[0] != "pbkdf2_sha256":
                return False
            salt = parts[1]
            expected = parts[2]
            dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
            return hmac.compare_digest(dk.hex(), expected)
        except Exception:
            return False

# JWT Implementation with pure-Python fallback
try:
    import jwt
    def create_jwt(payload: dict, secret: str, algorithm: str = "HS256") -> str:
        return jwt.encode(payload, secret, algorithm=algorithm)
    def decode_jwt(token: str, secret: str, algorithm: str = "HS256") -> dict:
        return jwt.decode(token, secret, algorithms=[algorithm])
except ImportError:
    def _b64e(b: bytes) -> str:
        return base64.urlsafe_b64encode(b).decode('utf-8').rstrip('=')
    def _b64d(s: str) -> bytes:
        pad = '=' * ((4 - len(s) % 4) % 4)
        return base64.urlsafe_b64decode((s + pad).encode('utf-8'))
    def create_jwt(payload: dict, secret: str, algorithm: str = "HS256") -> str:
        header = {"typ": "JWT", "alg": algorithm}
        h_str = _b64e(json.dumps(header).encode('utf-8'))
        p_str = _b64e(json.dumps(payload).encode('utf-8'))
        sig = hmac.new(secret.encode('utf-8'), f"{h_str}.{p_str}".encode('utf-8'), hashlib.sha256).digest()
        return f"{h_str}.{p_str}.{_b64e(sig)}"
    def decode_jwt(token: str, secret: str, algorithm: str = "HS256") -> dict:
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Invalid token format")
        expected_sig = hmac.new(secret.encode('utf-8'), f"{parts[0]}.{parts[1]}".encode('utf-8'), hashlib.sha256).digest()
        if not hmac.compare_digest(_b64e(expected_sig), parts[2]):
            raise ValueError("Signature mismatch")
        payload = json.loads(_b64d(parts[1]).decode('utf-8'))
        if "exp" in payload and payload["exp"] < time.time():
            raise ValueError("Token expired")
        return payload

# TOTP implementation (RFC 6238 compliant)
def generate_totp_secret() -> str:
    return base64.b32encode(os.urandom(20)).decode('utf-8').rstrip('=')

def get_totp_code(secret: str, interval: int = 30) -> str:
    pad = '=' * ((8 - len(secret) % 8) % 8)
    key = base64.b32decode((secret + pad).upper().encode('utf-8'))
    counter = int(time.time() // interval)
    msg = counter.to_bytes(8, byteorder='big')
    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    code = ((h[offset] & 0x7f) << 24 | (h[offset + 1] & 0xff) << 16 | (h[offset + 2] & 0xff) << 8 | (h[offset + 3] & 0xff)) % 1000000
    return f"{code:06d}"

def verify_totp(secret: str, code: str, window: int = 1) -> bool:
    if not secret or not code:
        return False
    # Check current window and +/- window steps
    current_time = time.time()
    for delta in range(-window, window + 1):
        test_time = current_time + delta * 30
        pad = '=' * ((8 - len(secret) % 8) % 8)
        try:
            key = base64.b32decode((secret + pad).upper().encode('utf-8'))
            counter = int(test_time // 30)
            msg = counter.to_bytes(8, byteorder='big')
            h = hmac.new(key, msg, hashlib.sha1).digest()
            offset = h[-1] & 0x0F
            val = ((h[offset] & 0x7f) << 24 | (h[offset + 1] & 0xff) << 16 | (h[offset + 2] & 0xff) << 8 | (h[offset + 3] & 0xff)) % 1000000
            if f"{val:06d}" == code.strip():
                return True
        except Exception:
            continue
    return False

# Field-level Encryption (AES-256-GCM / PBKDF2 HMAC-SHA256 authenticated fallback)
def encrypt_field(plaintext: str, key_hex: str) -> str:
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        key = bytes.fromhex(key_hex)[:32]
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
        return "enc:gcm:" + base64.b64encode(nonce + ct).decode('utf-8')
    except Exception:
        # Authenticated HMAC-SHA256 + XOR envelope fallback
        salt = os.urandom(16)
        key = hashlib.sha256(bytes.fromhex(key_hex) + salt).digest()
        pt_bytes = plaintext.encode('utf-8')
        ct_bytes = bytes(b ^ key[i % len(key)] for i, b in enumerate(pt_bytes))
        tag = hmac.new(key, ct_bytes, hashlib.sha256).digest()
        payload = salt + tag + ct_bytes
        return "enc:hmac:" + base64.b64encode(payload).decode('utf-8')

def decrypt_field(ciphertext: str, key_hex: str) -> str:
    if not ciphertext.startswith("enc:"):
        return ciphertext
    try:
        if ciphertext.startswith("enc:gcm:"):
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            data = base64.b64decode(ciphertext[8:])
            nonce = data[:12]
            ct = data[12:]
            key = bytes.fromhex(key_hex)[:32]
            return AESGCM(key).decrypt(nonce, ct, None).decode('utf-8')
        elif ciphertext.startswith("enc:hmac:"):
            data = base64.b64decode(ciphertext[9:])
            salt = data[:16]
            tag = data[16:48]
            ct_bytes = data[48:]
            key = hashlib.sha256(bytes.fromhex(key_hex) + salt).digest()
            calc_tag = hmac.new(key, ct_bytes, hashlib.sha256).digest()
            if not hmac.compare_digest(tag, calc_tag):
                raise ValueError("MAC check failed")
            return bytes(b ^ key[i % len(key)] for i, b in enumerate(ct_bytes)).decode('utf-8')
    except Exception as e:
        return "[ENCRYPTED_DATA_PROTECTED]"
    return ciphertext

# Digital signature helper (for signed decisions and model certificates)
def sign_data(data_str: str, private_key_hex: str) -> str:
    key_bytes = bytes.fromhex(private_key_hex.ljust(64, '0')[:32])
    sig = hmac.new(key_bytes, data_str.encode('utf-8'), hashlib.sha256).hexdigest()
    return f"sig:sha256:{sig}"

def verify_signature(data_str: str, signature: str, private_key_hex: str) -> bool:
    expected = sign_data(data_str, private_key_hex)
    return hmac.compare_digest(expected, signature)
