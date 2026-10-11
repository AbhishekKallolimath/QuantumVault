
import pytest

from crypto_engine import (
    generate_recipient_keypair,
    export_public_key,
    export_encrypted_private_key,
    import_public_key,
    import_encrypted_private_key,
    encrypt_message,
    decrypt_message,
)


def test_public_key_export_import():
    private_key = generate_recipient_keypair()
    public_key = private_key.public_key()

    exported = export_public_key(public_key)
    imported = import_public_key(exported)

    message = "Public key import works"
    envelope = encrypt_message(message, imported)

    assert decrypt_message(envelope, private_key) == message


def test_encrypted_private_key_export_import():
    private_key = generate_recipient_keypair()
    password = "QuantumVault123"

    exported = export_encrypted_private_key(
        private_key, password
    )
    imported = import_encrypted_private_key(
        exported, password
    )

    message = "Private key import works"
    envelope = encrypt_message(
        message, imported.public_key()
    )

    assert decrypt_message(envelope, imported) == message


def test_wrong_password_is_rejected():
    private_key = generate_recipient_keypair()
    exported = export_encrypted_private_key(
        private_key, "QuantumVault123"
    )

    with pytest.raises(Exception):
        import_encrypted_private_key(
            exported, "WrongPassword123"
        )


def test_mismatched_key_pair_is_detected():
    first_private = generate_recipient_keypair()
    second_private = generate_recipient_keypair()

    envelope = encrypt_message(
        "Test message",
        first_private.public_key(),
    )

    with pytest.raises(Exception):
        decrypt_message(envelope, second_private)


def test_invalid_public_key_file_is_rejected():
    with pytest.raises(Exception):
        import_public_key(b"not a valid public key")


def test_invalid_private_key_file_is_rejected():
    with pytest.raises(Exception):
        import_encrypted_private_key(
            b"not a valid private key",
            "QuantumVault123",
        )
