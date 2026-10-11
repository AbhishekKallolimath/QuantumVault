
import pytest

from benchmark_engine import benchmark_message


def test_benchmark_returns_valid_results():
    result = benchmark_message(message_size=100, repetitions=2)

    assert result["message_size_bytes"] == 100
    assert result["repetitions"] == 2
    assert result["encryption_median_ms"] >= 0
    assert result["decryption_median_ms"] >= 0
    assert result["verification"] == "passed"


def test_benchmark_rejects_zero_message_size():
    with pytest.raises(ValueError):
        benchmark_message(message_size=0, repetitions=1)


def test_benchmark_rejects_zero_repetitions():
    with pytest.raises(ValueError):
        benchmark_message(message_size=100, repetitions=0)


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

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(results[0].keys()) if results else [
                "message_size_bytes",
                "repetitions",
                "encryption_median_ms",
                "decryption_median_ms",
                "verification",
            ],
        )
        writer.writeheader()
        writer.writerows(results)

    return results
