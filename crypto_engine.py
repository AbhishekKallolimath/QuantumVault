
"""
QuantumVault — Cryptography Engine

Uses ML-KEM-768 for shared-secret establishment,
HKDF-SHA256 for key derivation, and AES-256-GCM
for authenticated message encryption.
"""

import base64
import os
import hashlib
import hmac
import os
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


# Domain separation: identifies keys derived for QuantumVault.
KDF_INFO = b"QuantumVault-v1-AES-256-GCM"
AAD = b"QuantumVault:message:v1"


def _encode(data: bytes) -> str:
    """Convert binary data into text suitable for JSON."""
    return base64.b64encode(data).decode("ascii")


def _decode(data: str) -> bytes:
    """Convert Base64 text back into binary data."""
    return base64.b64decode(data, validate=True)


def generate_recipient_keypair():
    """Generate the recipient's ML-KEM-768 private key."""
    return mlkem.MLKEM768PrivateKey.generate()


def export_public_key(public_key) -> bytes:
    """Export the recipient's public key."""
    from cryptography.hazmat.primitives import serialization

    return public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )



def export_encrypted_private_key(private_key, password: str) -> bytes:
    """Export the private key encrypted with a user-supplied password."""
    from cryptography.hazmat.primitives import serialization

    if not isinstance(password, str) or len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")

    encryption = serialization.BestAvailableEncryption(
        password.encode("utf-8")
    )

    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption,
    )



def import_public_key(key_data: bytes):
    """Load a recipient's public key from DER data."""
    from cryptography.hazmat.primitives import serialization

    key = serialization.load_der_public_key(key_data)

    if not isinstance(key, mlkem.MLKEM768PublicKey):
        raise ValueError("The file does not contain an ML-KEM-768 public key.")

    return key



def import_encrypted_private_key(pem_data: bytes, password: str):
    """Load a password-protected ML-KEM-768 private key."""
    from cryptography.hazmat.primitives import serialization

    if not isinstance(password, str) or not password:
        raise ValueError("A password is required.")

    key = serialization.load_pem_private_key(
        pem_data,
        password=password.encode("utf-8"),
    )

    if not isinstance(key, mlkem.MLKEM768PrivateKey):
        raise ValueError("The file does not contain an ML-KEM-768 private key.")

    return key



def _derive_aes_key(shared_secret: bytes, salt: bytes) -> bytes:
    """Derive a 256-bit AES key from the ML-KEM shared secret."""
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=KDF_INFO,
    ).derive(shared_secret)


def encrypt_message(message: str, recipient_public_key) -> dict:
    """
    Establish a shared secret and encrypt a message.

    The returned envelope contains public transmission data,
    not the recipient's private key or the shared secret.
    """
    if not isinstance(message, str):
        raise TypeError("Message must be a string.")

    # Establish the shared secret and encapsulate it.
    shared_secret, kem_ciphertext = recipient_public_key.encapsulate()

    # Derive an AES-256 key; never use the shared secret directly.
    salt = os.urandom(16)
    aes_key = _derive_aes_key(shared_secret, salt)

    # AES-GCM requires a unique nonce for each encryption with a key.
    nonce = os.urandom(12)
    encrypted = AESGCM(aes_key).encrypt(
        nonce,
        message.encode("utf-8"),
        AAD,
    )

    # Store binary fields as Base64 so the envelope is JSON-friendly.
    return {
        "version": 1,
        "algorithm": "ML-KEM-768 + HKDF-SHA256 + AES-256-GCM",
        "kem_ciphertext": _encode(kem_ciphertext),
        "kdf_salt": _encode(salt),
        "nonce": _encode(nonce),
        "ciphertext": _encode(encrypted),
    }


def decrypt_message(envelope: dict, recipient_private_key) -> str:
    """
    Recover a message using the recipient's ML-KEM private key.

    AES-GCM raises InvalidTag if the ciphertext, nonce, or
    authenticated data is incorrect.
    """
    if envelope.get("version") != 1:
        raise ValueError("Unsupported envelope version.")

    kem_ciphertext = _decode(envelope["kem_ciphertext"])
    salt = _decode(envelope["kdf_salt"])
    nonce = _decode(envelope["nonce"])
    ciphertext = _decode(envelope["ciphertext"])

    # Recover the same shared secret.
    shared_secret = recipient_private_key.decapsulate(kem_ciphertext)

    # Derive the same AES key and authenticate before returning plaintext.
    aes_key = _derive_aes_key(shared_secret, salt)
    plaintext = AESGCM(aes_key).decrypt(nonce, ciphertext, AAD)

    return plaintext.decode("utf-8")


def tamper_with_ciphertext(envelope: dict) -> dict:
    """Create a modified copy for the educational tampering demo."""
    tampered = envelope.copy()
    ciphertext = bytearray(_decode(envelope["ciphertext"]))

    if not ciphertext:
        raise ValueError("There is no ciphertext to modify.")

    # Flip one bit. Do not modify the original envelope.
    ciphertext[0] ^= 1
    tampered["ciphertext"] = _encode(bytes(ciphertext))

    return tampered
def encrypt_file(file_bytes: bytes, filename: str, recipient_public_key) -> dict:
    """Encrypt file bytes using ML-KEM-768 and AES-256-GCM."""

    if not isinstance(file_bytes, bytes):
        raise TypeError("file_bytes must be bytes.")

    if not filename or not isinstance(filename, str):
        raise ValueError("A valid filename is required.")

    # Keep only the filename, not any directory path.
    filename = os.path.basename(filename)

    shared_secret, kem_ciphertext = recipient_public_key.encapsulate()

    salt = os.urandom(16)
    nonce = os.urandom(12)

    aes_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b"QuantumVault-file-v1-AES-256-GCM",
    ).derive(shared_secret)

    aad = b"QuantumVault:file:v1:" + filename.encode("utf-8")

    encrypted_bytes = AESGCM(aes_key).encrypt(
        nonce, file_bytes, aad
    )

    return {
        "version": 1,
        "type": "file",
        "algorithm": "ML-KEM-768 + HKDF-SHA256 + AES-256-GCM",
        "filename": filename,
        "original_size": len(file_bytes),
        "sha256": hashlib.sha256(file_bytes).hexdigest(),
        "kem_ciphertext": base64.b64encode(kem_ciphertext).decode("ascii"),
        "kdf_salt": base64.b64encode(salt).decode("ascii"),
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "ciphertext": base64.b64encode(encrypted_bytes).decode("ascii"),
    }


def decrypt_file(envelope: dict, recipient_private_key) -> tuple[bytes, str]:
    """Authenticate and decrypt a QuantumVault file envelope."""

    if envelope.get("version") != 1 or envelope.get("type") != "file":
        raise ValueError("Unsupported or invalid file envelope.")

    filename = envelope.get("filename")

    if not isinstance(filename, str) or not filename:
        raise ValueError("Invalid filename.")

    if filename != os.path.basename(filename):
        raise ValueError("Unsafe filename.")

    try:
        kem_ciphertext = base64.b64decode(
            envelope["kem_ciphertext"], validate=True
        )
        salt = base64.b64decode(
            envelope["kdf_salt"], validate=True
        )
        nonce = base64.b64decode(
            envelope["nonce"], validate=True
        )
        ciphertext = base64.b64decode(
            envelope["ciphertext"], validate=True
        )
    except (KeyError, ValueError, TypeError) as exc:
        raise ValueError("Malformed encrypted file envelope.") from exc

    if len(salt) != 16 or len(nonce) != 12:
        raise ValueError("Invalid salt or nonce length.")

    shared_secret = recipient_private_key.decapsulate(kem_ciphertext)

    aes_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b"QuantumVault-file-v1-AES-256-GCM",
    ).derive(shared_secret)

    aad = b"QuantumVault:file:v1:" + filename.encode("utf-8")

    # Raises InvalidTag if the encrypted contents or authenticated
    # filename were modified.
    plaintext = AESGCM(aes_key).decrypt(
        nonce, ciphertext, aad
    )

    expected_hash = envelope.get("sha256")
    actual_hash = hashlib.sha256(plaintext).hexdigest()

    if not isinstance(expected_hash, str) or not hmac.compare_digest(
        expected_hash, actual_hash
    ):
        raise ValueError("SHA-256 integrity verification failed.")

    if envelope.get("original_size") != len(plaintext):
        raise ValueError("File size verification failed.")

    return plaintext, filename
