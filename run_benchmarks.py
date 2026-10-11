
"""Run QuantumVault message and file benchmarks."""

from benchmark_engine import (
    run_benchmark_suite,
    run_file_benchmark_suite,
)


def main():
    print("\nQUANTUMVAULT PERFORMANCE BENCHMARKS")
    print("=" * 65)

    message_results = run_benchmark_suite(repetitions=10)

    print("\nMESSAGE ENCRYPTION")
    print("-" * 65)

    for result in message_results:
        print(
            f"Size: {result['message_size_bytes']:>7} bytes | "
            f"Encrypt: {result['encryption_median_ms']:>9} ms | "
            f"Decrypt: {result['decryption_median_ms']:>9} ms | "
            f"Verification: {result['verification']}"
        )

    file_results = run_file_benchmark_suite(repetitions=10)

    print("\nFILE ENCRYPTION")
    print("-" * 85)

    for result in file_results:
        print(
            f"Size: {result['file_size_bytes']:>9} bytes | "
            f"Encrypt: {result['encryption_median_ms']:>8} ms | "
            f"Decrypt: {result['decryption_median_ms']:>8} ms | "
            f"Encrypt speed: {result['encryption_throughput_mb_s']:>7} MB/s | "
            f"Verification: {result['verification']}"
        )

    print("\nBenchmark CSV files:")
    print(" - results/message_benchmarks.csv")
    print(" - results/file_benchmarks.csv")


if __name__ == "__main__":
    main()
