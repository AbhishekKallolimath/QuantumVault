
from benchmark_engine import run_benchmark_suite


def main():
    results = run_benchmark_suite(repetitions=10)

    print("\nQuantumVault Message Benchmark Results")
    print("-" * 65)

    for result in results:
        print(
            f"Size: {result['message_size_bytes']:>7} bytes | "
            f"Encryption: {result['encryption_median_ms']:>9} ms | "
            f"Decryption: {result['decryption_median_ms']:>9} ms | "
            f"Verification: {result['verification']}"
        )

    print("\nCSV saved to: results/message_benchmarks.csv")


if __name__ == "__main__":
    main()
