
"""Benchmark QuantumVault message encryption and decryption."""

from statistics import median
from time import perf_counter

from crypto_engine import (
    decrypt_message,
    encrypt_message,
    generate_recipient_keypair,
)


def benchmark_message(
    message_size: int,
    repetitions: int = 10,
) -> dict:
    """Measure message encryption and decryption performance.

    Args:
        message_size: Number of UTF-8 bytes in the test message.
        repetitions: Number of encryption/decryption measurements.

    Returns:
        A dictionary containing input size and timing statistics.
    """
    if message_size < 1:
        raise ValueError("Message size must be at least 1 byte.")

    if repetitions < 1:
        raise ValueError("Repetitions must be at least 1.")

    private_key = generate_recipient_keypair()
    public_key = private_key.public_key()

    # Generate a deterministic UTF-8 test message of the requested size.
    message_bytes = b"A" * message_size
    message = message_bytes.decode("utf-8")

    encryption_times = []
    decryption_times = []

    for _ in range(repetitions):
        start = perf_counter()
        envelope = encrypt_message(message, public_key)
        encryption_times.append(perf_counter() - start)

        start = perf_counter()
        recovered_message = decrypt_message(envelope, private_key)
        decryption_times.append(perf_counter() - start)

        if recovered_message != message:
            raise RuntimeError("Benchmark verification failed.")

    return {
        "message_size_bytes": message_size,
        "repetitions": repetitions,
        "encryption_median_ms": round(
            median(encryption_times) * 1000, 4
        ),
        "decryption_median_ms": round(
            median(decryption_times) * 1000, 4
        ),
        "verification": "passed",
    }

import csv
from pathlib import Path


def run_benchmark_suite(
    message_sizes=(100, 1024, 10240, 102400),
    repetitions=10,
    output_file="results/message_benchmarks.csv",
) -> list[dict]:
    """Benchmark multiple message sizes and save results to CSV."""
    results = []

    for size in message_sizes:
        result = benchmark_message(
            message_size=size,
            repetitions=repetitions,
        )
        results.append(result)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "message_size_bytes",
        "repetitions",
        "encryption_median_ms",
        "decryption_median_ms",
        "verification",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    return results
