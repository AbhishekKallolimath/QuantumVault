
from crypto_engine import (
    generate_recipient_keypair,
    export_public_key,
    export_encrypted_private_key,
    import_public_key,
    import_encrypted_private_key,
    encrypt_message,
    decrypt_message,
)

# Generate a new key pair
private_key = generate_recipient_keypair()
public_key = private_key.public_key()

# Export both keys
public_pem = export_public_key(public_key)
private_pem = export_encrypted_private_key(
    private_key, "QuantumVault123"
)

# Import the saved keys
loaded_public_key = import_public_key(public_pem)
loaded_private_key = import_encrypted_private_key(
    private_pem, "QuantumVault123"
)

# Test encryption and decryption using imported keys
message = "QuantumVault key management works!"

envelope = encrypt_message(message, loaded_public_key)
decrypted_message = decrypt_message(envelope, loaded_private_key)

assert decrypted_message == message

print("Public key export/import: PASSED")
print("Encrypted private key export/import: PASSED")
print("Message encryption/decryption with imported keys: PASSED")
