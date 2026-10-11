
"""Security evaluation tests for QuantumVault."""

from copy import deepcopy

from cryptography.exceptions import InvalidTag

from crypto_engine import (
    decrypt_file,
    decrypt_message,
    encrypt_file,
    encrypt_message,
    generate_recipient_keypair,
    tamper_with_ciphertext,
)


def evaluate_security() -> list[dict]:
    """Run controlled security checks and return a report."""

    results = []

    def record(test_name: str, passed: bool, details: str) -> None:
        results.append(
            {
                "test": test_name,
                "status": "PASSED" if passed else "FAILED",
                "details": details,
            }
        )

    private_key = generate_recipient_keypair()
    public_key = private_key.public_key()

    wrong_private_key = generate_recipient_keypair()
    wrong_public_key = wrong_private_key.public_key()

    # Prepare a valid encrypted message.
    message = "QuantumVault security evaluation"
    envelope = encrypt_message(message, public_key)

    # Test 1: A legitimate recipient can decrypt the message.
    try:
        recovered = decrypt_message(envelope, private_key)
        record(
            "Valid message decryption",
            recovered == message,
            "Original message was recovered correctly."
            if recovered == message
            else "Recovered message did not match the original.",
        )
    except Exception as exc:
        record(
            "Valid message decryption",
            False,
            f"Unexpected error: {type(exc).__name__}",
        )

    # Test 2: Modified ciphertext must be rejected.
    try:
        modified = tamper_with_ciphertext(envelope)
        decrypt_message(modified, private_key)
        record(
            "Ciphertext tampering detection",
            False,
            "Modified ciphertext was incorrectly accepted.",
        )
    except (InvalidTag, ValueError):
        record(
            "Ciphertext tampering detection",
            True,
            "Modified ciphertext was rejected.",
        )
    except Exception as exc:
        record(
            "Ciphertext tampering detection",
            False,
            f"Unexpected error: {type(exc).__name__}",
        )

    # Test 3: An unrelated private key must not recover the message.
    try:
        decrypt_message(envelope, wrong_private_key)
        record(
            "Wrong private key rejection",
            False,
            "Decryption unexpectedly succeeded with an unrelated key.",
        )
    except Exception:
        record(
            "Wrong private key rejection",
            True,
            "Unrelated private key could not recover the message.",
        )

    # Test 4: Unsupported envelope versions must be rejected.
    try:
        invalid_version = deepcopy(envelope)
        invalid_version["version"] = 999
        decrypt_message(invalid_version, private_key)
        record(
            "Envelope version validation",
            False,
            "Unsupported envelope version was accepted.",
        )
    except ValueError:
        record(
            "Envelope version validation",
            True,
            "Unsupported envelope version was rejected.",
        )
    except Exception as exc:
        record(
            "Envelope version validation",
            False,
            f"Unexpected error: {type(exc).__name__}",
        )

    # Prepare a valid encrypted file.
    file_content = b"QuantumVault file integrity test"
    file_envelope = encrypt_file(
        file_content,
        "security_test.txt",
        public_key,
    )

    # Test 5: Modified encrypted file data must be rejected.
    try:
        modified_file = tamper_with_ciphertext(file_envelope)
        decrypt_file(modified_file, private_key)
        record(
            "File ciphertext tampering detection",
            False,
            "Modified file ciphertext was incorrectly accepted.",
        )
    except (InvalidTag, ValueError):
        record(
            "File ciphertext tampering detection",
            True,
            "Modified file ciphertext was rejected.",
        )
    except Exception as exc:
        record(
            "File ciphertext tampering detection",
            False,
            f"Unexpected error: {type(exc).__name__}",
        )

    # Test 6: Changing the authenticated filename must be rejected.
    try:
        renamed_file = deepcopy(file_envelope)
        renamed_file["filename"] = "renamed.txt"
        decrypt_file(renamed_file, private_key)
        record(
            "File metadata authentication",
            False,
            "Modified filename was incorrectly accepted.",
        )
    except (InvalidTag, ValueError):
        record(
            "File metadata authentication",
            True,
            "Modified authenticated filename was rejected.",
        )
    except Exception as exc:
        record(
            "File metadata authentication",
            False,
            f"Unexpected error: {type(exc).__name__}",
        )

    # Test 7: Invalid file envelope versions must be rejected.
    try:
        invalid_file = deepcopy(file_envelope)
        invalid_file["version"] = 999
        decrypt_file(invalid_file, private_key)
        record(
            "File envelope validation",
            False,
            "Unsupported file envelope version was accepted.",
        )
    except ValueError:
        record(
            "File envelope validation",
            True,
            "Unsupported file envelope version was rejected.",
        )
    except Exception as exc:
        record(
            "File envelope validation",
            False,
            f"Unexpected error: {type(exc).__name__}",
        )

    return results


if __name__ == "__main__":
    report = evaluate_security()

    print("\nQUANTUMVAULT SECURITY EVALUATION")
    print("=" * 65)

    for result in report:
        print(f"[{result['status']}] {result['test']}")
        print(f"         {result['details']}")

    passed = sum(result["status"] == "PASSED" for result in report)
    total = len(report)

    print("-" * 65)
    print(f"Result: {passed}/{total} checks passed")
