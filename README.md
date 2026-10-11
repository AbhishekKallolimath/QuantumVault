# 🔐 QuantumVault

### A Post-Quantum Cryptographic Framework for Secure Message Exchange and Integrity Verification

QuantumVault is an interactive cybersecurity project that demonstrates secure message exchange, file encryption, cryptographic integrity verification, and post-quantum key establishment.

The project uses **ML-KEM-768, HKDF-SHA256, and AES-256-GCM** to demonstrate how cryptographic components can work together to protect messages and files. It also includes security evaluation tests and performance benchmarks.

## Problem Statement

Traditional public-key cryptographic algorithms, including RSA and elliptic-curve cryptography (ECC), may be vulnerable to attacks from sufficiently powerful quantum computers. This creates a need to explore cryptographic algorithms designed to resist known quantum attacks.

QuantumVault demonstrates a post-quantum cryptographic workflow for establishing shared secrets, encrypting data, and detecting unauthorized modifications.

## Objectives

- Demonstrate secure message encryption and decryption.
- Explore post-quantum key establishment using ML-KEM-768.
- Derive encryption keys using HKDF-SHA256.
- Protect messages and files using AES-256-GCM.
- Demonstrate ciphertext interception and tampering detection.
- Implement public-key and encrypted private-key management.
- Evaluate security checks and measure cryptographic performance.

## Key Features

### 🔒 Secure Message Exchange
Encrypt and decrypt messages using the project's post-quantum cryptographic workflow.

### 🕵️ Interception Lab
Inspect intercepted encrypted data and understand why ciphertext should not reveal the original plaintext.

### ⚛️ Quantum Threat Awareness
Explore the potential implications of quantum computing for traditional public-key cryptography.

### 📁 File Encryption Lab
Encrypt and decrypt files and demonstrate detection of modified ciphertext and authenticated metadata.

### 🔑 Key Management
Export and import public keys and manage encrypted private-key files with password-based protection.

### 🛡️ Security Evaluation
Run automated security checks covering valid decryption, ciphertext tampering, incorrect private keys, envelope validation, and file security.

### 📊 Performance Dashboard
Visualize message and file encryption/decryption timings and file throughput using benchmark results.

## Cryptographic Workflow

1. Establish a shared secret using ML-KEM-768.
2. Derive a symmetric encryption key using HKDF-SHA256.
3. Encrypt the message or file using AES-256-GCM.
4. Transmit or inspect the encrypted data.
5. Decrypt the data using the appropriate private key and cryptographic information.
6. Verify authenticity and integrity through authenticated decryption.
7. Reject modified ciphertext or invalid authenticated data.

## Technology Stack

- **Language:** Python
- **Interface:** Streamlit
- **Post-quantum cryptography:** ML-KEM-768
- **Key derivation:** HKDF-SHA256
- **Authenticated encryption:** AES-256-GCM
- **Data analysis:** Pandas
- **Visualizations:** Plotly
- **Testing:** Pytest
- **Version control:** Git and GitHub

## Project Structure

```text
QuantumVault/
├── app.py
├── crypto_engine.py
├── security_evaluator.py
├── benchmark_engine.py
├── run_benchmarks.py
├── performance_dashboard.py
├── tests/
│   ├── test_crypto.py
│   ├── test_file_crypto.py
│   ├── test_key_management.py
│   └── test_benchmark.py
├── results/
│   ├── message_benchmarks.csv
│   └── file_benchmarks.csv
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.10 or a compatible version supported by the installed dependencies.
- Git.
- A virtual environment is recommended.

### 1. Clone the repository

```bash
git clone https://github.com/AbhishekKallolimath/QuantumVault.git
cd QuantumVault
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the dependencies listed in your project's dependency file, if available. If the project does not yet have one, create a `requirements.txt` containing the packages and versions used by the working environment before sharing the project.

### 4. Run the application

```powershell
streamlit run app.py
```

### 5. Run automated tests

```powershell
python -m pytest -v
```

### 6. Generate benchmark results

```powershell
python run_benchmarks.py
```

The benchmark script generates message and file benchmark CSVs in the `results/` directory.

### 7. Run the standalone performance dashboard

```powershell
streamlit run performance_dashboard.py
```

## Testing and Evaluation

The current automated test suite contains **19 passing tests** covering:

- Message encryption and decryption.
- Ciphertext tampering detection.
- Rejection of incorrect private keys.
- File encryption and decryption.
- File tampering detection.
- Public-key import and export.
- Encrypted private-key import and export.
- Password validation and key-pair consistency.
- Benchmark validation and CSV generation.

The security evaluation module includes seven checks covering message and file security scenarios. The performance dashboard displays benchmark results generated on the local machine.

Benchmark timings and throughput may vary with hardware, software versions, and test configuration. They should be treated as experimental measurements rather than universal performance guarantees.

## Educational Scope and Limitations

QuantumVault is an educational and experimental project, not a production-ready secure messaging platform.

- It does not implement an actual quantum computer.
- It does not demonstrate breaking RSA or ECC.
- Its security depends on the correctness of the implementation, key handling, and deployment environment.
- Benchmark results do not independently establish cryptographic security.
- The project should undergo further security review before any real-world deployment.

## Future Improvements

- Add reproducible benchmark configurations and comparative analysis.
- Expand negative testing and malformed-input handling.
- Improve key lifecycle management and security documentation.
- Add application screenshots and architecture diagrams.
- Evaluate additional post-quantum cryptographic configurations.

## Author

**Abhishek Kallolimath**

GitHub: [AbhishekKallolimath](https://github.com/AbhishekKallolimath)
