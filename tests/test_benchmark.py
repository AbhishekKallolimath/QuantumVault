
import pytest

from benchmark_engine import (
    benchmark_file,
    benchmark_message,
    run_file_benchmark_suite,
)


def test_benchmark_returns_valid_results():
    result = benchmark_message(
        message_size=100,
        repetitions=2,
        warmups=1,
    )

    assert result["message_size_bytes"] == 100
    assert result["repetitions"] == 2
    assert result["warmup_runs"] == 1
    assert result["encryption_min_ms"] >= 0
    assert result["encryption_median_ms"] >= 0
    assert result["encryption_p95_ms"] >= 0
    assert result["decryption_min_ms"] >= 0
    assert result["decryption_median_ms"] >= 0
    assert result["decryption_p95_ms"] >= 0
    assert result["verification"] == "passed"


def test_benchmark_rejects_zero_message_size():
    with pytest.raises(ValueError):
        benchmark_message(message_size=0, repetitions=1)


def test_benchmark_rejects_zero_repetitions():
    with pytest.raises(ValueError):
        benchmark_message(message_size=100, repetitions=0)


def test_benchmark_rejects_negative_warmups():
    with pytest.raises(ValueError):
        benchmark_message(
            message_size=100,
            repetitions=1,
            warmups=-1,
        )


def test_file_benchmark_returns_valid_results():
    result = benchmark_file(
        file_size=1024,
        repetitions=2,
        warmups=1,
    )

    assert result["file_size_bytes"] == 1024
    assert result["repetitions"] == 2
    assert result["warmup_runs"] == 1
    assert result["encryption_median_ms"] >= 0
    assert result["decryption_median_ms"] >= 0
    assert result["encryption_throughput_mb_s"] > 0
    assert result["decryption_throughput_mb_s"] > 0
    assert result["verification"] == "passed"


def test_file_benchmark_rejects_zero_size():
    with pytest.raises(ValueError):
        benchmark_file(file_size=0, repetitions=1)


def test_file_benchmark_suite_creates_csv(tmp_path):
    output_file = tmp_path / "file_benchmarks.csv"

    results = run_file_benchmark_suite(
        file_sizes=(100, 1024),
        repetitions=1,
        warmups=0,
        output_file=str(output_file),
    )

    assert len(results) == 2
    assert output_file.exists()

    contents = output_file.read_text(encoding="utf-8")
    assert "file_size_bytes" in contents
    assert "encryption_throughput_mb_s" in contents
    assert "verification" in contents
