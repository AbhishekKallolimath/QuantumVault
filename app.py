
import base64
import json
import streamlit as st

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import serialization

from crypto_engine import (
    generate_recipient_keypair,
    encrypt_message,
    decrypt_message,
    tamper_with_ciphertext,
    encrypt_file,
    decrypt_file,
)

st.set_page_config(
    page_title="QuantumVault",
    page_icon="🔐",
    layout="wide",
)

st.title("🔐 QuantumVault")
st.caption(
    "A Post-Quantum Cryptographic Framework for "
    "Secure Message Exchange and Integrity Verification"
)

# Keep the demo recipient's keys available during this session.
if "recipient_private_key" not in st.session_state:
    st.session_state.recipient_private_key = generate_recipient_keypair()

private_key = st.session_state.recipient_private_key
public_key = private_key.public_key()

secure_tab, intercept_tab, threat_tab, file_tab = st.tabs(
    [
        "🔒 Secure Message",
        "🕵️ Interception Lab",
        "⚛️ Quantum Threat",
        "📁 File Encryption Lab",
    ]
)

# --------------------------------------------------
# TAB 1: SECURE MESSAGE
# --------------------------------------------------
with secure_tab:
    st.subheader("Secure Message Exchange")
    st.write("Encrypt a message using the recipient's public key.")

    message = st.text_area(
        "Enter your message",
        placeholder="Type a confidential message...",
        key="message_input",
    )

    if st.button("Encrypt Message", key="encrypt_message"):
        if not message:
            st.warning("Please enter a message first.")
        else:
            try:
                envelope = encrypt_message(message, public_key)
                st.session_state.message_envelope = envelope
                st.success("Message encrypted successfully.")
            except Exception as exc:
                st.error(f"Encryption failed: {exc}")

    if "message_envelope" in st.session_state:
        envelope = st.session_state.message_envelope

        st.markdown("**Encrypted envelope**")
        st.json(envelope)

        if st.button("Decrypt Message", key="decrypt_message"):
            try:
                plaintext = decrypt_message(envelope, private_key)
                st.success("Message decrypted successfully.")
                st.text_area(
                    "Recovered message",
                    value=plaintext,
                    disabled=True,
                    key="recovered_message",
                )
            except Exception as exc:
                st.error(f"Decryption failed: {exc}")


# --------------------------------------------------
# TAB 2: INTERCEPTION LAB
# --------------------------------------------------
with intercept_tab:
    st.subheader("Interception and Tampering Demonstration")
    st.write(
        "Modify an encrypted message to demonstrate how "
        "AES-GCM authentication detects tampering."
    )

    if "message_envelope" not in st.session_state:
        st.info("First encrypt a message in the Secure Message tab.")
    else:
        if st.button("Simulate Ciphertext Tampering"):
            st.session_state.tampered_envelope = tamper_with_ciphertext(
                st.session_state.message_envelope
            )

        if "tampered_envelope" in st.session_state:
            st.markdown("**Tampered encrypted envelope**")
            st.json(st.session_state.tampered_envelope)

            if st.button("Attempt to Decrypt Tampered Message"):
                try:
                    decrypt_message(
                        st.session_state.tampered_envelope,
                        private_key,
                    )
                    st.error("Unexpected result: tampering was not detected.")
                except (InvalidTag, ValueError):
                    st.success(
                        "Tampering detected. The modified message "
                        "failed authentication."
                    )
                except Exception as exc:
                    st.error(f"Decryption rejected: {exc}")


# --------------------------------------------------
# TAB 3: QUANTUM THREAT
# --------------------------------------------------
with threat_tab:
    st.subheader("Why Post-Quantum Cryptography?")
    st.write(
        "A sufficiently capable quantum computer could threaten "
        "some public-key cryptographic systems currently in use."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Traditional approach")
        st.write(
            "- RSA and elliptic-curve cryptography are widely used.\n"
            "- Large-scale quantum computers could threaten their "
            "underlying mathematical assumptions."
        )

    with col2:
        st.markdown("### QuantumVault approach")
        st.write(
            "- ML-KEM-768 establishes a shared secret.\n"
            "- HKDF-SHA256 derives an encryption key.\n"
            "- AES-256-GCM encrypts data and authenticates it."
        )

    st.info(
        "QuantumVault is an educational prototype. It demonstrates "
        "post-quantum key establishment, authenticated encryption, "
        "and tampering detection; it is not a certified security product."
    )


# --------------------------------------------------
# TAB 4: FILE ENCRYPTION LAB
# --------------------------------------------------
with file_tab:
    st.subheader("File Encryption and Decryption")
    st.write(
        "Encrypt a file into a JSON envelope, then import that "
        "envelope to recover the original file."
    )

    encrypt_col, decrypt_col = st.columns(2)

    with encrypt_col:
        st.markdown("### Encrypt a file")

        uploaded_file = st.file_uploader(
            "Choose a file to encrypt",
            key="file_to_encrypt",
        )

        if st.button("Encrypt File", key="encrypt_file_button"):
            if uploaded_file is None:
                st.warning("Please choose a file first.")
            else:
                try:
                    file_bytes = uploaded_file.getvalue()

                    file_envelope = encrypt_file(
                        file_bytes,
                        uploaded_file.name,
                        public_key,
                    )

                    st.session_state.file_envelope = file_envelope
                    st.success("File encrypted successfully.")

                except Exception as exc:
                    st.error(f"File encryption failed: {exc}")

        if "file_envelope" in st.session_state:
            file_envelope = st.session_state.file_envelope

            st.write(f"**Original filename:** {file_envelope['filename']}")
            st.write(f"**Original size:** {file_envelope['original_size']} bytes")
            st.write(f"**SHA-256:** `{file_envelope['sha256']}`")

            json_bytes = json.dumps(
                file_envelope,
                indent=2,
            ).encode("utf-8")

            st.download_button(
                "Download Encrypted JSON",
                data=json_bytes,
                file_name=file_envelope["filename"] + ".qvault.json",
                mime="application/json",
                key="download_encrypted_file",
            )

    with decrypt_col:
        st.markdown("### Decrypt an encrypted file")

        uploaded_envelope = st.file_uploader(
            "Choose a QuantumVault JSON envelope",
            type=["json"],
            key="file_envelope_upload",
        )

        if st.button("Decrypt File", key="decrypt_file_button"):
            if uploaded_envelope is None:
                st.warning("Please upload an encrypted JSON envelope.")
            else:
                try:
                    imported_envelope = json.loads(
                        uploaded_envelope.getvalue().decode("utf-8")
                    )

                    plaintext, original_filename = decrypt_file(
                        imported_envelope,
                        private_key,
                    )

                    st.session_state.decrypted_file_bytes = plaintext
                    st.session_state.decrypted_filename = original_filename

                    st.success("File decrypted and integrity verified.")

                except (InvalidTag, ValueError, KeyError, TypeError) as exc:
                    st.error(
                        "Decryption or verification failed. Check the "
                        "envelope and make sure it was encrypted for "
                        f"this recipient. Details: {exc}"
                    )
                except Exception as exc:
                    st.error(f"File decryption failed: {exc}")

        if "decrypted_file_bytes" in st.session_state:
            st.download_button(
                "Download Decrypted File",
                data=st.session_state.decrypted_file_bytes,
                file_name=st.session_state.decrypted_filename,
                mime="application/octet-stream",
                key="download_decrypted_file",
            )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.caption(
    "QuantumVault | ML-KEM-768 • HKDF-SHA256 • AES-256-GCM"
)
