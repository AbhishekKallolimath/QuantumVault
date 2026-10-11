
import base64
import json
import streamlit as st

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import serialization
from security_evaluator import evaluate_security
from performance_dashboard import render_performance_dashboard

from crypto_engine import (
    generate_recipient_keypair,
    encrypt_message,
    decrypt_message,
    tamper_with_ciphertext,
    encrypt_file,
    decrypt_file,
    export_public_key,
    export_encrypted_private_key,
    import_public_key,
    import_encrypted_private_key,
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



secure_tab, intercept_tab, threat_tab, file_tab, key_tab, security_tab, performance_tab = st.tabs(
    [
        "🔒 Secure Message",
        "🕵️ Interception Lab",
        "⚛️ Quantum Threat",
        "📁 File Encryption Lab",
        "🔑 Key Management",
        "🛡️ Security Evaluation",
        "📊 Performance Dashboard",
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
# TAB 5: KEY MANAGEMENT
# --------------------------------------------------
with key_tab:
    st.subheader("Cryptographic Key Management")
    st.write(
        "Export your keys for backup or import previously saved keys."
    )

    st.warning(
        "Keep your private key confidential. Never upload it to GitHub "
        "or share it with anyone."
    )

    # ----------------------------------------------
    # EXPORT KEYS
    # ----------------------------------------------
    st.markdown("### Export current keys")

    password = st.text_input(
        "Set a password for your private-key backup",
        type="password",
        key="export_key_password",
        help="Use at least 8 characters.",
    )

    confirm_password = st.text_input(
        "Confirm password",
        type="password",
        key="confirm_key_password",
    )

    if st.button("Prepare Key Downloads", key="prepare_key_downloads"):
        if len(password) < 8:
            st.error("Password must contain at least 8 characters.")

        elif password != confirm_password:
            st.error("The passwords do not match.")

        else:
            try:
                exported_public = export_public_key(public_key)
                exported_private = export_encrypted_private_key(
                    private_key, password
                )

                st.session_state["exported_public_key"] = exported_public
                st.session_state["exported_private_key"] = exported_private

                st.success("Your key backups are ready.")

            except Exception:
                st.error("Key export failed. Please check the key implementation.")

    if (
        "exported_public_key" in st.session_state
        and "exported_private_key" in st.session_state
    ):
        st.download_button(
            "Download Public Key",
            data=st.session_state["exported_public_key"],
            file_name="quantumvault_public.der",
            mime="application/octet-stream",
            key="download_public_key",
        )

        st.download_button(
            "Download Password-Protected Private Key",
            data=st.session_state["exported_private_key"],
            file_name="quantumvault_private.pem",
            mime="application/octet-stream",
            key="download_private_key",
        )

    st.divider()

    # ----------------------------------------------
    # IMPORT KEYS
    # ----------------------------------------------
    st.markdown("### Import saved keys")

    uploaded_public_key = st.file_uploader(
        "Upload public key (.der)",
        key="import_public_key_file",
    )

    uploaded_private_key = st.file_uploader(
        "Upload encrypted private key (.pem)",
        key="import_private_key_file",
    )

    import_password = st.text_input(
        "Private-key backup password",
        type="password",
        key="import_key_password",
    )

    if st.button("Import and Activate Keys", key="activate_imported_keys"):
        if uploaded_public_key is None or uploaded_private_key is None:
            st.error("Please upload both key files.")

        elif not import_password:
            st.error("Enter the private-key backup password.")

        else:
            try:
                new_public_key = import_public_key(
                    uploaded_public_key.getvalue()
                )

                new_private_key = import_encrypted_private_key(
                    uploaded_private_key.getvalue(),
                    import_password,
                )

                # Verify that the uploaded keys belong together.
                test_message = "QuantumVault key-pair verification"

                test_envelope = encrypt_message(
                    test_message,
                    new_public_key,
                )

                recovered_message = decrypt_message(
                    test_envelope,
                    new_private_key,
                )

                if recovered_message != test_message:
                    raise ValueError("The uploaded keys do not match.")

                # Activate the verified private key.
                st.session_state["recipient_private_key"] = new_private_key

                # Remove results associated with the previous key.
                keys_to_clear = [
                    "message_envelope",
                    "tampered_envelope",
                    "file_envelope",
                    "decrypted_file_bytes",
                    "decrypted_filename",
                    "exported_public_key",
                    "exported_private_key",
                ]

                for key in keys_to_clear:
                    st.session_state.pop(key, None)

                st.success(
                    "Keys imported and verified. The new key pair is active."
                )

                st.rerun()

            except Exception:
                st.error(
                    "Key import failed. Check the key files and password, "
                    "and make sure the public and private keys match."
                )


# --------------------------------------------------
# TAB 6: SECURITY EVALUATION
# --------------------------------------------------

with security_tab:
    st.subheader("🛡️ Automated Security Evaluation")

    st.write(
        "Run controlled tests to check whether QuantumVault "
        "rejects tampered data, incorrect keys, and invalid envelopes."
    )

    st.warning(
        "These checks demonstrate selected security properties. "
        "They are not a complete security audit."
    )

    if st.button("▶️ Run Security Evaluation", key="run_security_evaluation"):
        try:
            with st.spinner("Running security checks..."):
                results = evaluate_security()

            st.session_state["security_evaluation_results"] = results

        except Exception as exc:
            st.error(f"Security evaluation could not complete: {exc}")

    if "security_evaluation_results" in st.session_state:
        results = st.session_state["security_evaluation_results"]

        passed = sum(
            result["status"] == "PASSED"
            for result in results
        )
        total = len(results)
        failed = total - passed

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Checks", total)
        col2.metric("Passed", passed)
        col3.metric("Failed", failed)

        if total > 0 and failed == 0:
            st.success(f"All {passed} security checks passed.")
        elif failed > 0:
            st.error(f"{failed} security check(s) failed.")
        else:
            st.info("No security checks were returned.")

        st.markdown("### Detailed Results")

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True,
        )

        import pandas as pd

        csv_data = pd.DataFrame(results).to_csv(index=False)

        st.download_button(
            "⬇️ Download Security Report (CSV)",
            data=csv_data,
            file_name="quantumvault_security_report.csv",
            mime="text/csv",
            key="download_security_report",
        )

with performance_tab:
    render_performance_dashboard()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.caption(
    "QuantumVault | ML-KEM-768 • HKDF-SHA256 • AES-256-GCM"
)
