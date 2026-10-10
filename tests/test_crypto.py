
import pytest
from cryptography.exceptions import InvalidTag

from crypto_engine import (
    generate_recipient_keypair,
    encrypt_message,
    decrypt_message,
    tamper_with_ciphertext,
)


def test_message_encrypts_and_decrypts():
    key = generate_recipient_keypair()
    message = "QuantumVault confidential message"

    envelope = encrypt_message(message, key.public_key())
    recovered = decrypt_message(envelope, key)

    assert recovered == message


def test_tampered_ciphertext_is_rejected():
    key = generate_recipient_keypair()
    envelope = encrypt_message("Secret mission", key.public_key())
    tampered = tamper_with_ciphertext(envelope)

    with pytest.raises(InvalidTag):
        decrypt_message(tampered, key)


def test_wrong_private_key_cannot_decrypt():
    recipient = generate_recipient_keypair()
    other_person = generate_recipient_keypair()

    envelope = encrypt_message(
        "Confidential information",
        recipient.public_key(),
    )

    with pytest.raises(InvalidTag):
        decrypt_message(envelope, other_person)
