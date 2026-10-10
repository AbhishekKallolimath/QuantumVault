
import pytest
from cryptography.exceptions import InvalidTag

from crypto_engine import (
    generate_recipient_keypair,
    encrypt_file,
    decrypt_file,
)


def test_file_encryption_and_decryption():
    recipient_private_key = generate_recipient_keypair()
    recipient_public_key = recipient_private_key.public_key()

    original_data = b"QuantumVault file encryption test.\x00\x01\x02"
    envelope = encrypt_file(
        original_data,
        "secret.bin",
        recipient_public_key,
    )

    recovered_data, recovered_filename = decrypt_file(
        envelope,
        recipient_private_key,
    )

    assert recovered_data == original_data
    assert recovered_filename == "secret.bin"


def test_tampered_file_is_rejected():
    recipient_private_key = generate_recipient_keypair()
    envelope = encrypt_file(
        b"Secret file contents",
        "secret.txt",
        recipient_private_key.public_key(),
    )

    # Alter the ciphertext without changing the authentication tag.
    import base64

    ciphertext = bytearray(
        base64.b64decode(envelope["ciphertext"])
    )
    ciphertext[0] ^= 1

    envelope["ciphertext"] = base64.b64encode(
        ciphertext
    ).decode("ascii")

    with pytest.raises(InvalidTag):
        decrypt_file(envelope, recipient_private_key)


def test_wrong_private_key_is_rejected():
    recipient1 = generate_recipient_keypair()
    recipient2 = generate_recipient_keypair()

    envelope = encrypt_file(
        b"Only recipient 1 should decrypt this",
        "private.txt",
        recipient1.public_key(),
    )

    with pytest.raises((InvalidTag, ValueError)):
        decrypt_file(envelope, recipient2)
