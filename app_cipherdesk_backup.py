
import streamlit as st

from crypto_engine import encrypt_text, decrypt_text


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CipherDesk | Secure Text",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM UI THEME
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&display=swap');

    .stApp {
        background: #080d18;
        color: #e8eef8;
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stSidebar"] {
        background: #0c1423;
        border-right: 1px solid #243249;
    }

    .brand {
        font-size: 27px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .brand span {
        color: #a3ff70;
    }

    .muted {
        color: #91a0b7;
        font-size: 13px;
    }

    .eyebrow {
        color: #a3ff70;
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        letter-spacing: 2px;
    }

    .hero {
        padding: 18px 0 24px 0;
    }

    .hero h1 {
        font-size: clamp(32px, 4vw, 48px);
        line-height: 1.12;
        letter-spacing: -2px;
        font-weight: 800;
        color: #f1f5fb;
        margin: 12px 0;
    }

    .hero h1 span {
        color: #a3ff70;
    }

    .metric-card {
        background: #101a2a;
        border: 1px solid #243249;
        border-radius: 13px;
        padding: 17px;
        min-height: 100px;
    }

    .metric-label {
        color: #91a0b7;
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        letter-spacing: 1px;
    }

    .metric-value {
        color: #a3ff70;
        font-size: 18px;
        font-weight: 700;
        margin-top: 10px;
    }

    .info-card {
        background: #101a2a;
        border: 1px solid #243249;
        border-radius: 13px;
        padding: 20px;
        margin: 12px 0;
    }

    .info-card h3 {
        color: #a3ff70;
        font-size: 18px;
    }

    .stTextArea textarea,
    .stTextInput input {
        background: #0a1220 !important;
        color: #f1f5fb !important;
        border: 1px solid #2b3b53 !important;
        border-radius: 9px !important;
    }

    .stTextArea textarea:focus,
    .stTextInput input:focus {
        border-color: #a3ff70 !important;
        box-shadow: 0 0 0 1px #a3ff70 !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        background: #a3ff70;
        color: #0a1220;
        border: none;
        border-radius: 9px;
        font-weight: 800;
        min-height: 43px;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: #c0ff9d;
        color: #080d18;
        border: none;
    }

    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        font-weight: 600;
    }

    hr {
        border-color: #243249;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        '<div class="brand">CIPHER<span>DESK</span></div>',
        unsafe_allow_html=True,
    )

    st.caption("SECURE TEXT WORKSPACE")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Encrypt Text",
            "Decrypt Text",
            "Security Overview",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### Active algorithms")

    st.markdown(
        """
        <div class="muted">
        ● AES-256-GCM<br><br>
        ● Scrypt key derivation<br><br>
        ● Random salt and nonce
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.caption("Python · Streamlit · Cryptography")


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">PRIVATE COMMUNICATIONS / TOOL 01</div>
        <h1>Your message.<br><span>Your control.</span></h1>
        <div class="muted">
            Transform readable text into authenticated ciphertext
            and recover it with the correct password.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# ALGORITHM CARDS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">ENCRYPTION</div>
            <div class="metric-value">AES-256-GCM</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">KEY DERIVATION</div>
            <div class="metric-value">SCRYPT</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">DATA INTEGRITY</div>
            <div class="metric-value">AUTHENTICATED</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")


# --------------------------------------------------
# PAGE 1: ENCRYPT TEXT
# --------------------------------------------------

if page == "Encrypt Text":

    st.markdown(
        '<div class="eyebrow">01 / ENCRYPTION WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    st.subheader("Protect a message")
    st.caption(
        "Enter your text and a strong password to generate an encrypted payload."
    )

    with st.container(border=True):

        message = st.text_area(
            "PLAINTEXT MESSAGE",
            placeholder="Type your private message here...",
            height=180,
            key="plaintext_input",
        )

        password = st.text_input(
            "ENCRYPTION PASSWORD",
            type="password",
            placeholder="Use a strong password",
            key="encrypt_password",
        )

        encrypt_clicked = st.button(
            "🔒  ENCRYPT MESSAGE",
            type="primary",
            use_container_width=True,
        )

        if encrypt_clicked:

            st.session_state.pop("cipher_result", None)

            if not message:
                st.error("Please enter a message.")

            elif len(password) < 12:
                st.error(
                    "Please use a password with at least 12 characters."
                )

            else:
                try:
                    encrypted = encrypt_text(message, password)
                    st.session_state["cipher_result"] = encrypted
                    st.success("Message encrypted successfully.")

                except Exception:
                    st.error(
                        "Encryption failed. Check your input and try again."
                    )

    if "cipher_result" in st.session_state:

        st.markdown("### Encrypted payload")
        st.caption(
            "This encoded output contains the encrypted message and the "
            "metadata needed for decryption. It does not contain your password."
        )

        st.code(
            st.session_state["cipher_result"],
            language="text",
        )

        st.download_button(
            "⬇️ Download encrypted text",
            data=st.session_state["cipher_result"],
            file_name="encrypted_message.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.info(
            "Keep the encrypted output and password separately. "
            "You need both to recover your message."
        )


# --------------------------------------------------
# PAGE 2: DECRYPT TEXT
# --------------------------------------------------

elif page == "Decrypt Text":

    st.markdown(
        '<div class="eyebrow">02 / DECRYPTION WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    st.subheader("Recover your original message")
    st.caption(
        "Paste the complete encrypted payload and provide the original password."
    )

    with st.container(border=True):

        encrypted_input = st.text_area(
            "ENCRYPTED PAYLOAD",
            placeholder="Paste your encrypted text here...",
            height=180,
            key="ciphertext_input",
        )

        password = st.text_input(
            "DECRYPTION PASSWORD",
            type="password",
            placeholder="Enter the original password",
            key="decrypt_password",
        )

        decrypt_clicked = st.button(
            "🔓  DECRYPT MESSAGE",
            type="primary",
            use_container_width=True,
        )

        if decrypt_clicked:

            st.session_state.pop("plain_result", None)

            if not encrypted_input.strip():
                st.error("Please paste the encrypted payload.")

            elif not password:
                st.error("Please enter the decryption password.")

            else:
                try:
                    plaintext = decrypt_text(
                        encrypted_input.strip(),
                        password,
                    )

                    st.session_state["plain_result"] = plaintext
                    st.success("Message decrypted successfully.")

                except ValueError as exc:
                    st.error(str(exc))

                except Exception:
                    st.error(
                        "Unable to decrypt this input. Check the payload "
                        "and try again."
                    )

    if "plain_result" in st.session_state:

        st.markdown("### Recovered message")

        st.text_area(
            "DECRYPTED PLAINTEXT",
            value=st.session_state["plain_result"],
            height=180,
            disabled=True,
        )

        st.download_button(
            "⬇️ Download recovered message",
            data=st.session_state["plain_result"],
            file_name="decrypted_message.txt",
            mime="text/plain",
            use_container_width=True,
        )


# --------------------------------------------------
# PAGE 3: SECURITY OVERVIEW
# --------------------------------------------------

else:

    st.markdown(
        '<div class="eyebrow">03 / SECURITY OVERVIEW</div>',
        unsafe_allow_html=True,
    )

    st.subheader("How the protection works")

    st.markdown(
        """
        <div class="info-card">
            <div class="eyebrow">LAYER 01</div>
            <h3>AES-256-GCM</h3>
            Encrypts the plaintext and authenticates the encrypted data.
            Changes to the ciphertext should cause authentication to fail.
        </div>

        <div class="info-card">
            <div class="eyebrow">LAYER 02</div>
            <h3>Scrypt password-based key derivation</h3>
            Derives a 256-bit key from the password and a random salt.
            Scrypt makes password guessing more computationally expensive.
        </div>

        <div class="info-card">
            <div class="eyebrow">LAYER 03</div>
            <h3>Random salt and nonce</h3>
            A fresh random salt and nonce are generated for each encryption.
            The salt is used for key derivation; the nonce is used by AES-GCM.
        </div>

        <div class="info-card">
            <div class="eyebrow">IMPORTANT</div>
            <h3>Use strong passwords</h3>
            A weak password can still be guessed. Keep your password private.
            Losing the password generally means losing access to the message.
            This educational project has not undergone a professional
            security audit.
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div class="muted">
        CIPHERDESK · SECURE TEXT ENCRYPTION TOOL<br>
        Built with Python, Streamlit and the Cryptography library.
    </div>
    """,
    unsafe_allow_html=True,
)
