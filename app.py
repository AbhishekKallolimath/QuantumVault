import base64
import json

import pandas as pd
import streamlit as st
from cryptography.exceptions import InvalidTag

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
    page_title="QuantumVault | Security Workspace",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------- DESIGN SYSTEM ----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --bg: #080d17;
        --surface: #101827;
        --surface-2: #131f31;
        --line: #26354a;
        --text: #edf3ff;
        --muted: #93a4bc;
        --cyan: #67e8f9;
        --blue: #818cf8;
        --green: #6ee7b7;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 10% 0%, rgba(37, 99, 150, .20), transparent 34%),
            radial-gradient(ellipse at 95% 12%, rgba(79, 70, 229, .12), transparent 27%),
            var(--bg);
        color: var(--text);
        font-family: 'DM Sans', sans-serif;
    }
    .block-container { max-width: 1500px; padding: 1.8rem 2.6rem 3rem; }
    header[data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: #0a111e;
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] > div { padding-top: 1.6rem; }
    h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif !important; color: var(--text) !important; }
    h1 { letter-spacing: -1.6px; font-weight: 700 !important; }
    h2, h3 { letter-spacing: -.5px; }
    p, label, .stCaption { color: var(--muted); }
    [data-testid="stMarkdownContainer"] p { line-height: 1.65; }

    .brand-row { display:flex; align-items:center; gap:13px; margin: 0 0 1.5rem 0; }
    .brand-mark {
        width:48px; height:48px; display:flex; align-items:center; justify-content:center;
        border-radius:15px; font-size:24px;
        background:linear-gradient(135deg,#164e63,#312e81);
        border:1px solid #3c718b; box-shadow:0 8px 30px rgba(34,211,238,.10);
    }
    .brand-name { font:700 25px 'Space Grotesk',sans-serif; color:#f4f7ff; letter-spacing:-1px; }
    .brand-sub { color:#91a4be; font-size:10px; letter-spacing:2px; margin-top:3px; }
    .status-pill {
        display:inline-flex; align-items:center; gap:8px; border-radius:999px;
        padding:8px 12px; border:1px solid #245448; background:#102a27;
        color:#8df2c8; font-size:11px; font-weight:700; letter-spacing:.4px;
    }
    .hero {
        position:relative; overflow:hidden; border-radius:24px; padding:31px 34px;
        border:1px solid #2a4261;
        background:linear-gradient(115deg,rgba(20,48,73,.97),rgba(16,24,39,.98) 65%,rgba(31,35,77,.88));
        margin: 0 0 24px 0;
    }
    .hero:after {
        content:""; position:absolute; width:250px; height:250px; right:-75px; top:-110px;
        border:1px solid rgba(103,232,249,.16); border-radius:50%;
        box-shadow:0 0 0 25px rgba(103,232,249,.025),0 0 0 55px rgba(103,232,249,.02);
    }
    .eyebrow { color:var(--cyan); font-size:10px; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin-bottom:12px; }
    .hero-title { color:#f6f8ff; font:700 clamp(28px,3.4vw,43px)/1.12 'Space Grotesk',sans-serif; letter-spacing:-1.6px; margin-bottom:14px; }
    .hero-copy { color:#a9bad0; max-width:690px; font-size:14px; line-height:1.8; }
    .section-label { color:#79dff0; font-size:10px; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin:25px 0 12px; }
    .metric-card {
        background:linear-gradient(145deg,#121f31,#0e1725);
        border:1px solid var(--line); border-radius:16px; padding:18px 19px;
        min-height:119px;
    }
    .metric-label { color:#94a7c0; font-size:10px; font-weight:700; letter-spacing:1.2px; }
    .metric-value { color:#f2f6ff; font:700 20px 'Space Grotesk',sans-serif; margin:12px 0 7px; }
    .metric-note { color:#71dcb6; font-size:11px; }
    .panel-note {
        border:1px solid var(--line); border-radius:13px; padding:14px 16px;
        background:rgba(16,24,39,.75); color:#a8b7cb; font-size:12px;
    }

    .stTabs [data-baseweb="tab-list"] { gap:7px; padding:7px 0 13px; border-bottom:1px solid var(--line); flex-wrap:wrap; }
    .stTabs [data-baseweb="tab"] {
        border:1px solid #28384e; border-radius:10px; padding:10px 13px;
        background:#101827; color:#a8b8ce; font-size:12px; font-weight:600;
    }
    .stTabs [aria-selected="true"] { background:#153345 !important; border-color:#32839a !important; color:#79edf5 !important; }
    .stButton > button, .stDownloadButton > button {
        min-height:42px; border-radius:10px; padding:8px 16px; font-weight:700;
        color:#f8fbff; border:1px solid #438ca5;
        background:linear-gradient(100deg,#176b83,#405fc0);
        transition:all .18s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        border-color:#8cecf4; color:white; transform:translateY(-1px);
    }
    .stTextInput input, .stTextArea textarea, [data-baseweb="select"] > div {
        background:#0c1421 !important; border-color:#2b3c53 !important; color:#eaf1ff !important; border-radius:10px !important;
    }
    [data-testid="stFileUploader"] {
        background:#0d1726; border:1px dashed #344a65; border-radius:14px; padding:12px;
    }
    [data-testid="stMetric"] { background:#111c2c; border:1px solid #29394f; border-radius:13px; padding:15px; }
    [data-testid="stMetricValue"] { color:#72e7f0; }
    [data-testid="stAlert"] { border-radius:12px; }
    .stDataFrame { border:1px solid var(--line); border-radius:12px; overflow:hidden; }
    hr { border-color:var(--line); }
    footer { visibility:hidden; }
    @media(max-width:800px) {
        .block-container { padding:1rem 1rem 2rem; }
        .hero { padding:23px; }
        .brand-name { font-size:22px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------- HEADER --------------------------------
header_left, header_right = st.columns([4, 1.25], vertical_alignment="center")
with header_left:
    st.markdown(
        """
        <div class="brand-row">
          <div class="brand-mark">🔐</div>
          <div>
            <div class="brand-name">QuantumVault</div>
            <div class="brand-sub">POST-QUANTUM SECURITY WORKSPACE</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with header_right:
    st.markdown(
        '<div style="text-align:right"><span class="status-pill">● SESSION ACTIVE</span></div>',
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Cryptography · Integrity · Resilience</div>
      <div class="hero-title">Security, engineered<br>for the quantum era.</div>
      <div class="hero-copy">
        A unified workspace for secure message exchange, file protection,
        key management and hands-on security evaluation. Explore post-quantum
        key establishment with ML-KEM-768 and authenticated encryption with AES-256-GCM.
      </div>
    </div>
    <div class="section-label">Cryptographic stack</div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)
for col, label, value, note in [
    (m1, "KEY ESTABLISHMENT", "ML-KEM-768", "Post-quantum key encapsulation"),
    (m2, "KEY DERIVATION", "HKDF-SHA256", "Cryptographic key derivation"),
    (m3, "DATA PROTECTION", "AES-256-GCM", "Encryption with authentication"),
    (m4, "WORKSPACE", "7 MODULES", "Encrypt · Inspect · Evaluate"),
]:
    with col:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">{label}</div>'
            f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-label">Workspace modules</div>', unsafe_allow_html=True)

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
        "📁 File Encryption",
        "🔑 Key Management",
        "🛡️ Security Evaluation",
        "📊 Performance",
    ]
)

# -------------------------- TAB 1: SECURE MESSAGE -----------------------
with secure_tab:
    st.subheader("Secure message exchange")
    st.caption("Encrypt a confidential message for the active recipient key.")

    message_col, info_col = st.columns([1.5, 1], gap="large")
    with message_col:
        message = st.text_area(
            "Message plaintext",
            placeholder="Type a confidential message...",
            height=180,
            key="message_input",
        )
        if st.button("Encrypt message", key="encrypt_message", type="primary"):
            if not message:
                st.warning("Please enter a message first.")
            else:
                try:
                    envelope = encrypt_message(message, public_key)
                    st.session_state.message_envelope = envelope
                    st.session_state.pop("tampered_envelope", None)
                    st.success("Message encrypted successfully.")
                except Exception as exc:
                    st.error(f"Encryption failed: {exc}")
    with info_col:
        st.markdown("#### Protection flow")
        st.markdown(
            """
            <div class="panel-note">
            <b>01 · Encapsulate</b><br>Establish a shared secret with ML-KEM-768.<br><br>
            <b>02 · Derive</b><br>Derive an encryption key using HKDF-SHA256.<br><br>
            <b>03 · Authenticate</b><br>Protect the message with AES-256-GCM.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if "message_envelope" in st.session_state:
        st.divider()
        st.markdown("#### Encrypted envelope")
        st.json(st.session_state.message_envelope, expanded=False)
        if st.button("Decrypt message", key="decrypt_message"):
            try:
                plaintext = decrypt_message(st.session_state.message_envelope, private_key)
                st.success("Message decrypted successfully.")
                st.text_area(
                    "Recovered plaintext",
                    value=plaintext,
                    disabled=True,
                    key="recovered_message",
                )
            except Exception as exc:
                st.error(f"Decryption failed: {exc}")

# -------------------------- TAB 2: INTERCEPTION -------------------------
with intercept_tab:
    st.subheader("Interception & tampering lab")
    st.caption("Simulate ciphertext modification and verify authenticated decryption rejects it.")
    if "message_envelope" not in st.session_state:
        st.info("Encrypt a message in the Secure Message module first.")
    else:
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown("#### Original envelope")
            st.json(st.session_state.message_envelope, expanded=False)
            if st.button("Simulate ciphertext tampering", key="tamper_button"):
                st.session_state.tampered_envelope = tamper_with_ciphertext(
                    st.session_state.message_envelope
                )
                st.success("A modified envelope is ready for testing.")
        with right:
            st.markdown("#### Modified envelope")
            if "tampered_envelope" in st.session_state:
                st.json(st.session_state.tampered_envelope, expanded=False)
                if st.button("Attempt authenticated decryption", key="decrypt_tampered"):
                    try:
                        decrypt_message(st.session_state.tampered_envelope, private_key)
                        st.error("Unexpected result: tampering was not detected.")
                    except (InvalidTag, ValueError):
                        st.success("Tampering detected. Authentication failed as expected.")
                    except Exception as exc:
                        st.error(f"Decryption rejected: {exc}")
            else:
                st.markdown(
                    '<div class="panel-note">The modified envelope will appear here after you simulate tampering.</div>',
                    unsafe_allow_html=True,
                )

# ---------------------------- TAB 3: THREAT -----------------------------
with threat_tab:
    st.subheader("Why post-quantum cryptography?")
    st.caption("Understand the motivation behind a cryptographic design built for future threats.")
    traditional, quantum = st.columns(2, gap="large")
    with traditional:
        st.markdown("#### Traditional public-key cryptography")
        st.markdown(
            """
            <div class="metric-card">
              <div class="metric-label">CURRENT APPROACH</div>
              <div class="metric-value">RSA · ECC</div>
              <p>Widely deployed public-key systems rely on mathematical problems that
              sufficiently capable quantum computers could threaten.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with quantum:
        st.markdown("#### QuantumVault architecture")
        st.markdown(
            """
            <div class="metric-card">
              <div class="metric-label">THIS PROTOTYPE</div>
              <div class="metric-value">PQC + AEAD</div>
              <p>ML-KEM-768 establishes a shared secret, HKDF-SHA256 derives a key,
              and AES-256-GCM encrypts data and authenticates its integrity.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.warning(
        "QuantumVault is an prototype. It demonstrates post-quantum key "
        "establishment, authenticated encryption and tampering detection."
    )

# ------------------------- TAB 4: FILE ENCRYPTION -----------------------
with file_tab:
    st.subheader("File encryption workspace")
    st.caption("Encrypt files into portable JSON envelopes or decrypt previously exported envelopes.")
    encrypt_col, decrypt_col = st.columns(2, gap="large")

    with encrypt_col:
        st.markdown("#### Encrypt a file")
        uploaded_file = st.file_uploader("Choose a file to encrypt", key="file_to_encrypt")
        if st.button("Encrypt file", key="encrypt_file_button", type="primary"):
            if uploaded_file is None:
                st.warning("Please choose a file first.")
            else:
                try:
                    file_envelope = encrypt_file(
                        uploaded_file.getvalue(), uploaded_file.name, public_key
                    )
                    st.session_state.file_envelope = file_envelope
                    st.success("File encrypted successfully.")
                except Exception as exc:
                    st.error(f"File encryption failed: {exc}")

        if "file_envelope" in st.session_state:
            file_envelope = st.session_state.file_envelope
            st.markdown("#### Encrypted file details")
            st.write(f"**Original filename:** {file_envelope['filename']}")
            st.write(f"**Original size:** {file_envelope['original_size']} bytes")
            st.code(file_envelope["sha256"], language="text")
            json_bytes = json.dumps(file_envelope, indent=2).encode("utf-8")
            st.download_button(
                "Download encrypted JSON",
                data=json_bytes,
                file_name=file_envelope["filename"] + ".qvault.json",
                mime="application/json",
                key="download_encrypted_file",
            )

    with decrypt_col:
        st.markdown("#### Decrypt an envelope")
        uploaded_envelope = st.file_uploader(
            "Choose a QuantumVault JSON envelope",
            type=["json"],
            key="file_envelope_upload",
        )
        if st.button("Decrypt file", key="decrypt_file_button", type="primary"):
            if uploaded_envelope is None:
                st.warning("Please upload an encrypted JSON envelope.")
            else:
                try:
                    imported_envelope = json.loads(
                        uploaded_envelope.getvalue().decode("utf-8")
                    )
                    plaintext, original_filename = decrypt_file(imported_envelope, private_key)
                    st.session_state.decrypted_file_bytes = plaintext
                    st.session_state.decrypted_filename = original_filename
                    st.success("File decrypted and integrity verified.")
                except (InvalidTag, ValueError, KeyError, TypeError) as exc:
                    st.error(
                        "Decryption or verification failed. Check the envelope and ensure "
                        f"it was encrypted for this recipient. Details: {exc}"
                    )
                except Exception as exc:
                    st.error(f"File decryption failed: {exc}")

        if "decrypted_file_bytes" in st.session_state:
            st.download_button(
                "Download decrypted file",
                data=st.session_state.decrypted_file_bytes,
                file_name=st.session_state.decrypted_filename,
                mime="application/octet-stream",
                key="download_decrypted_file",
            )

# --------------------------- TAB 5: KEY MANAGEMENT ----------------------
with key_tab:
    st.subheader("Cryptographic key management")
    st.caption("Create password-protected backups or activate a previously saved key pair.")
    st.warning("Keep your private key confidential. Never upload it to GitHub or share it.")

    st.markdown("#### Export current keys")
    export_col, export_help = st.columns([1.3, 1], gap="large")
    with export_col:
        password = st.text_input(
            "Backup password", type="password", key="export_key_password",
            help="Use at least 8 characters.",
        )
        confirm_password = st.text_input(
            "Confirm backup password", type="password", key="confirm_key_password"
        )
        if st.button("Prepare key downloads", key="prepare_key_downloads"):
            if len(password) < 8:
                st.error("Password must contain at least 8 characters.")
            elif password != confirm_password:
                st.error("The passwords do not match.")
            else:
                try:
                    st.session_state["exported_public_key"] = export_public_key(public_key)
                    st.session_state["exported_private_key"] = export_encrypted_private_key(
                        private_key, password
                    )
                    st.success("Your key backups are ready.")
                except Exception:
                    st.error("Key export failed. Please check the key implementation.")
    with export_help:
        st.markdown(
            """
            <div class="panel-note">
            <b>Key backup guidance</b><br><br>
            • Keep the private-key backup password safe.<br><br>
            • Store private-key backups in a secure location.<br><br>
            • A public key can be shared; a private key must remain confidential.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if "exported_public_key" in st.session_state and "exported_private_key" in st.session_state:
        public_download, private_download = st.columns(2)
        with public_download:
            st.download_button(
                "Download public key",
                data=st.session_state["exported_public_key"],
                file_name="quantumvault_public.der",
                mime="application/octet-stream",
                key="download_public_key",
            )
        with private_download:
            st.download_button(
                "Download password-protected private key",
                data=st.session_state["exported_private_key"],
                file_name="quantumvault_private.pem",
                mime="application/octet-stream",
                key="download_private_key",
            )

    st.divider()
    st.markdown("#### Import saved keys")
    import_col, import_help = st.columns([1.3, 1], gap="large")
    with import_col:
        uploaded_public_key = st.file_uploader(
            "Upload public key (.der)", key="import_public_key_file"
        )
        uploaded_private_key = st.file_uploader(
            "Upload encrypted private key (.pem)", key="import_private_key_file"
        )
        import_password = st.text_input(
            "Private-key backup password", type="password", key="import_key_password"
        )
        if st.button("Import and activate keys", key="activate_imported_keys"):
            if uploaded_public_key is None or uploaded_private_key is None:
                st.error("Please upload both key files.")
            elif not import_password:
                st.error("Enter the private-key backup password.")
            else:
                try:
                    new_public_key = import_public_key(uploaded_public_key.getvalue())
                    new_private_key = import_encrypted_private_key(
                        uploaded_private_key.getvalue(), import_password
                    )
                    test_message = "QuantumVault key-pair verification"
                    test_envelope = encrypt_message(test_message, new_public_key)
                    recovered_message = decrypt_message(test_envelope, new_private_key)
                    if recovered_message != test_message:
                        raise ValueError("The uploaded keys do not match.")

                    st.session_state["recipient_private_key"] = new_private_key
                    keys_to_clear = [
                        "message_envelope", "tampered_envelope", "file_envelope",
                        "decrypted_file_bytes", "decrypted_filename",
                        "exported_public_key", "exported_private_key",
                    ]
                    for key in keys_to_clear:
                        st.session_state.pop(key, None)
                    st.success("Keys imported and verified. The new key pair is active.")
                    st.rerun()
                except Exception:
                    st.error(
                        "Key import failed. Check the key files and password, and ensure "
                        "the public and private keys match."
                    )
    with import_help:
        st.markdown(
            """
            <div class="panel-note">
            <b>Activation safeguards</b><br><br>
            QuantumVault tests that the imported public and private keys match before
            activating the new private key. Previous message and file results are cleared
            after a successful key change.
            </div>
            """,
            unsafe_allow_html=True,
        )

# ------------------------- TAB 6: SECURITY EVALUATION -------------------
with security_tab:
    st.subheader("Automated security evaluation")
    st.caption("Run controlled checks for tampering, incorrect keys and invalid envelopes.")
    st.warning("These checks demonstrate selected security properties; they are not a complete security audit.")

    if st.button("Run security evaluation", key="run_security_evaluation", type="primary"):
        try:
            with st.spinner("Running security checks..."):
                results = evaluate_security()
            st.session_state["security_evaluation_results"] = results
        except Exception as exc:
            st.error(f"Security evaluation could not complete: {exc}")

    if "security_evaluation_results" in st.session_state:
        results = st.session_state["security_evaluation_results"]
        passed = sum(result["status"] == "PASSED" for result in results)
        total = len(results)
        failed = total - passed

        c1, c2, c3 = st.columns(3)
        c1.metric("Total checks", total)
        c2.metric("Passed", passed)
        c3.metric("Failed", failed)

        if total > 0 and failed == 0:
            st.success(f"All {passed} security checks passed.")
        elif failed > 0:
            st.error(f"{failed} security check(s) failed.")
        else:
            st.info("No security checks were returned.")

        st.markdown("#### Detailed results")
        st.dataframe(results, use_container_width=True, hide_index=True)
        csv_data = pd.DataFrame(results).to_csv(index=False)
        st.download_button(
            "Download security report (CSV)",
            data=csv_data,
            file_name="quantumvault_security_report.csv",
            mime="text/csv",
            key="download_security_report",
        )

# ------------------------- TAB 7: PERFORMANCE ---------------------------
with performance_tab:
    st.subheader("Performance dashboard")
    st.caption("Inspect the performance measurements available in this project.")
    render_performance_dashboard()

# -------------------------------- FOOTER -------------------------------
st.divider()
footer_left, footer_right = st.columns([3, 1])
with footer_left:
    st.caption("QUANTUMVAULT  ·  ML-KEM-768  ·  HKDF-SHA256  ·  AES-256-GCM")
with footer_right:
    st.markdown(
        '<div style="text-align:right;color:#63758e;font-size:11px">SECURITY PROTOTYPE</div>',
        unsafe_allow_html=True,
    )
