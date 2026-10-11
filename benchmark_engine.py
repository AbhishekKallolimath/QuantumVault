
"""Benchmark QuantumVault message and file encryption."""

import csv
from pathlib import Path
from statistics import median
from time import perf_counter

from crypto_engine import (
    decrypt_file,
    decrypt_message,
    encrypt_file,
    encrypt_message,
    generate_recipient_keypair,
)


def _timing_statistics(times: list[float]) -> dict:
    """Calculate timing statistics in milliseconds."""
    ordered = sorted(times)

    p95_index = max(0, int(0.95 * len(ordered) + 0.999999) - 1)

    return {
        "min_ms": round(ordered[0] * 1000, 4),
        "median_ms": round(median(ordered) * 1000, 4),
        "p95_ms": round(ordered[p95_index] * 1000, 4),
    }


def _validate_inputs(size: int, repetitions: int, warmups: int) -> None:
    if size < 1:
        raise ValueError("Input size must be at least 1 byte.")
    if repetitions < 1:
        raise ValueError("Repetitions must be at least 1.")
    if warmups < 0:
        raise ValueError("Warm-up runs cannot be negative.")


def benchmark_message(
    message_size: int,
    repetitions: int = 10,
    warmups: int = 2,
) -> dict:
    """Measure message encryption and decryption performance."""
    _validate_inputs(message_size, repetitions, warmups)

    private_key = generate_recipient_keypair()
    public_key = private_key.public_key()
    message = "A" * message_size

    encryption_times = []
    decryption_times = []

    # Warm-up measurements are excluded from the reported statistics.
    for run in range(warmups + repetitions):
        start = perf_counter()
        envelope = encrypt_message(message, public_key)
        encryption_time = perf_counter() - start

        start = perf_counter()
        recovered_message = decrypt_message(envelope, private_key)
        decryption_time = perf_counter() - start

        if recovered_message != message:
            raise RuntimeError("Benchmark verification failed.")

        if run >= warmups:
            encryption_times.append(encryption_time)
            decryption_times.append(decryption_time)

    encryption_stats = _timing_statistics(encryption_times)
    decryption_stats = _timing_statistics(decryption_times)

    return {
        "message_size_bytes": len(message.encode("utf-8")),
        "repetitions": repetitions,
        "warmup_runs": warmups,
        "encryption_min_ms": encryption_stats["min_ms"],
        "encryption_median_ms": encryption_stats["median_ms"],
        "encryption_p95_ms": encryption_stats["p95_ms"],
        "decryption_min_ms": decryption_stats["min_ms"],
        "decryption_median_ms": decryption_stats["median_ms"],
        "decryption_p95_ms": decryption_stats["p95_ms"],
        "verification": "passed",
    }


def benchmark_file(
    file_size: int,
    repetitions: int = 10,
    warmups: int = 2,
) -> dict:
    """Measure file encryption/decryption time and throughput."""
    _validate_inputs(file_size, repetitions, warmups)

    private_key = generate_recipient_keypair()
    public_key = private_key.public_key()
    file_bytes = b"A" * file_size
    filename = "benchmark_test.bin"

    encryption_times = []
    decryption_times = []

    for run in range(warmups + repetitions):
        start = perf_counter()
        envelope = encrypt_file(file_bytes, filename, public_key)
        encryption_time = perf_counter() - start

        start = perf_counter()
        recovered_bytes, recovered_filename = decrypt_file(
            envelope, private_key
        )
        decryption_time = perf_counter() - start

        if recovered_bytes != file_bytes or recovered_filename != filename:
            raise RuntimeError("File benchmark verification failed.")

        if run >= warmups:
            encryption_times.append(encryption_time)
            decryption_times.append(decryption_time)

    encryption_stats = _timing_statistics(encryption_times)
    decryption_stats = _timing_statistics(decryption_times)

    # Throughput uses the median operation time.
    encryption_seconds = encryption_stats["median_ms"] / 1000
    decryption_seconds = decryption_stats["median_ms"] / 1000
    size_mb = file_size / (1024 * 1024)

    return {
        "file_size_bytes": file_size,
        "repetitions": repetitions,
        "warmup_runs": warmups,
        "encryption_median_ms": encryption_stats["median_ms"],
        "encryption_p95_ms": encryption_stats["p95_ms"],
        "decryption_median_ms": decryption_stats["median_ms"],
        "decryption_p95_ms": decryption_stats["p95_ms"],
        "encryption_throughput_mb_s": round(
            size_mb / encryption_seconds, 4
        ) if encryption_seconds > 0 else 0,
        "decryption_throughput_mb_s": round(
            size_mb / decryption_seconds, 4
        ) if decryption_seconds > 0 else 0,
        "verification": "passed",
    }


def _save_csv(results: list[dict], output_file: str) -> None:
    """Save a list of benchmark records to CSV."""
    if not results:
        raise ValueError("Cannot save an empty benchmark result set.")

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(results[0].keys()),
        )
        writer.writeheader()
        writer.writerows(results)


def run_benchmark_suite(
    message_sizes=(100, 1024, 10240, 102400),
    repetitions=10,
    output_file="results/message_benchmarks.csv",
    warmups=2,
) -> list[dict]:
    """Benchmark multiple message sizes and save results to CSV."""
    results = [
        benchmark_message(size, repetitions, warmups)
        for size in message_sizes
    ]
    _save_csv(results, output_file)
    return results


def run_file_benchmark_suite(
    file_sizes=(1024, 10240, 102400, 1048576),
    repetitions=10,
    output_file="results/file_benchmarks.csv",
    warmups=2,
) -> list[dict]:
    """Benchmark multiple file sizes and save results to CSV."""
    results = [
        benchmark_file(size, repetitions, warmups)
        for size in file_sizes
    ]
    _save_csv(results, output_file)
    return results
