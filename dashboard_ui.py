
import streamlit as st


def apply_dashboard_style():
    st.markdown(
        """
        <style>
        @import url(
          'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
        );

        :root {
            --bg: #080d18;
            --panel: #101a2b;
            --border: #24334a;
            --text: #edf4ff;
            --muted: #94a7c2;
            --accent: #52e0c0;
            --blue: #68a9ff;
        }

        .stApp {
            background:
                radial-gradient(ellipse at 80% 0%,
                #142b40 0%, #080d18 48%);
            color: var(--text);
            font-family: 'Inter', sans-serif;
        }

        [data-testid="stSidebar"] {
            background: #0b1220;
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] * {
            font-family: 'Inter', sans-serif;
        }

        .block-container {
            max-width: 1450px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            color: var(--text) !important;
            letter-spacing: -0.6px;
        }

        p, label {
            color: #c4d0e1;
        }

        .brand {
            font-size: 25px;
            font-weight: 800;
            color: var(--text);
            letter-spacing: -1px;
        }

        .brand span {
            color: var(--accent);
        }

        .eyebrow {
            color: var(--accent);
            text-transform: uppercase;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
        }

        .hero {
            padding: 28px;
            border: 1px solid #29445b;
            border-radius: 20px;
            background: linear-gradient(
                120deg, #13263b 0%, #101a2b 60%,
                #102a30 100%
            );
            margin-bottom: 25px;
        }

        .hero h1 {
            font-size: 35px;
            line-height: 1.2;
            margin: 10px 0;
        }

        .hero p {
            color: var(--muted);
            max-width: 680px;
            line-height: 1.7;
        }

        .metric {
            background: linear-gradient(145deg, #121f32, #0e1726);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            min-height: 145px;
        }

        .metric-label {
            color: var(--muted);
            font-size: 13px;
            margin-bottom: 13px;
        }

        .metric-value {
            font-size: 21px;
            font-weight: 800;
            color: var(--text);
            overflow-wrap: anywhere;
        }

        .metric-note {
            color: var(--accent);
            font-size: 12px;
            margin-top: 10px;
        }

        .section-title {
            font-size: 20px;
            font-weight: 700;
            margin: 28px 0 14px;
            color: var(--text);
        }

        .feature {
            background: #101a2b;
            border: 1px solid var(--border);
            border-radius: 15px;
            padding: 20px;
            min-height: 150px;
        }

        .feature-icon {
            font-size: 24px;
            margin-bottom: 12px;
        }

        .feature-title {
            font-size: 15px;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 8px;
        }

        .feature-desc {
            font-size: 12px;
            line-height: 1.6;
            color: var(--muted);
        }

        .notice {
            background: #101f2c;
            border: 1px solid #254c53;
            border-radius: 12px;
            padding: 16px;
            color: #b8d5dc;
            font-size: 13px;
            line-height: 1.7;
        }

        div.stButton > button {
            border-radius: 10px;
            min-height: 43px;
            font-weight: 600;
            border: 1px solid #2a4258;
            transition: all .2s ease;
        }

        div.stButton > button[kind="primary"] {
            background: var(--accent);
            color: #061511;
            border: none;
        }

        div.stButton > button:hover {
            border-color: var(--accent);
            transform: translateY(-1px);
        }

        [data-testid="stMetric"] {
            background: #101a2b;
            border: 1px solid var(--border);
            padding: 15px;
            border-radius: 12px;
        }

        [data-testid="stMetricValue"] {
            color: var(--text);
        }

        hr {
            border-color: var(--border);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard():
    apply_dashboard_style()

    with st.sidebar:
        st.markdown(
            '<div class="brand">Quantum<span>Vault</span></div>',
            unsafe_allow_html=True,
        )
        st.caption("POST-QUANTUM SECURITY PLATFORM")
        st.divider()

        st.markdown("### Navigation")
        page = st.radio(
            "Navigate",
            [
                "Dashboard",
                "Secure Message",
                "Interception Lab",
                "Quantum Threat",
                "File Encryption Lab",
                "Key Management",
                "Security Evaluation",
                "Performance Dashboard",
            ],
            label_visibility="collapsed",
            key="qv_navigation",
        )

        st.divider()
        st.caption("CRYPTOGRAPHIC ARCHITECTURE")
        st.markdown("`ML-KEM-768`")
        st.markdown("`HKDF-SHA256`")
        st.markdown("`AES-256-GCM`")
        st.caption("Local application interface")

    if page != "Dashboard":
        st.info(
            f"Selected: {page}. Connect this selection to the "
            "corresponding existing page in app.py."
        )
        return

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">SECURITY CONTROL CENTER</div>
            <h1>Welcome to QuantumVault</h1>
            <p>
                A post-quantum cryptographic framework for secure
                message exchange, file protection, and integrity
                verification. Manage your security tools from one place.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">Cryptographic Overview</div>',
        unsafe_allow_html=True,
    )

    metrics = [
        ("KEY ENCAPSULATION", "ML-KEM-768", "Post-quantum algorithm"),
        ("KEY DERIVATION", "HKDF-SHA256", "Derived symmetric key"),
        ("DATA ENCRYPTION", "AES-256-GCM", "Authenticated encryption"),
        ("INTEGRITY", "Authentication tag", "Tampering detection"),
    ]

    columns = st.columns(4)

    for column, (label, value, note) in zip(columns, metrics):
        with column:
            st.markdown(
                f"""
                <div class="metric">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-note">◆ {note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title">Security Workspaces</div>',
        unsafe_allow_html=True,
    )

    features = [
        (
            "🔐",
            "Secure Message",
            "Encrypt messages for a recipient and decrypt "
            "them with the corresponding private key.",
        ),
        (
            "🧪",
            "Interception Lab",
            "Explore ciphertext modification and authenticated "
            "decryption failure.",
        ),
        (
            "📁",
            "File Encryption",
            "Protect files using the application's existing "
            "file-encryption workflow.",
        ),
        (
            "🗝️",
            "Key Management",
            "Import, export, and manage cryptographic keys.",
        ),
        (
            "🛡️",
            "Security Evaluation",
            "Review the security checks implemented in the project.",
        ),
        (
            "📊",
            "Performance Analytics",
            "Review available encryption benchmarks and metrics.",
        ),
    ]

    for start in range(0, len(features), 3):
        cols = st.columns(3)

        for col, feature in zip(cols, features[start:start + 3]):
            icon, title, description = feature

            with col:
                st.markdown(
                    f"""
                    <div class="feature">
                        <div class="feature-icon">{icon}</div>
                        <div class="feature-title">{title}</div>
                        <div class="feature-desc">{description}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("")
    st.markdown(
        """
        <div class="notice">
            <strong>Security note</strong><br>
            This dashboard describes the configured cryptographic
            components. It does not independently verify the security
            of the complete system or guarantee protection against
            every attack.
        </div>
        """,
        unsafe_allow_html=True,
    )
