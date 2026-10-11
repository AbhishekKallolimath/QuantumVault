
"""Performance dashboard for QuantumVault benchmarks."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

RESULTS_DIR = Path(__file__).parent / "results"
MESSAGE_CSV = RESULTS_DIR / "message_benchmarks.csv"
FILE_CSV = RESULTS_DIR / "file_benchmarks.csv"


def load_results(path: Path) -> pd.DataFrame:
    """Load benchmark results if the CSV exists."""
    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except (OSError, pd.errors.ParserError, UnicodeDecodeError):
        return pd.DataFrame()


def render_performance_dashboard() -> None:
    """Render charts and tables for benchmark results."""

    st.subheader("📊 QuantumVault Performance Dashboard")
    st.write(
        "Explore encryption and decryption latency and file throughput "
        "from the latest benchmark runs."
    )

    message_df = load_results(MESSAGE_CSV)
    file_df = load_results(FILE_CSV)

    if message_df.empty and file_df.empty:
        st.info(
            "No benchmark results found. Run `python run_benchmarks.py` "
            "in your project terminal, then refresh this page."
        )
        return

    if not message_df.empty:
        required = {
            "message_size_bytes",
            "encryption_median_ms",
            "decryption_median_ms",
        }

        if required.issubset(message_df.columns):
            st.markdown("### Message encryption")

            message_chart = message_df.melt(
                id_vars=["message_size_bytes"],
                value_vars=[
                    "encryption_median_ms",
                    "decryption_median_ms",
                ],
                var_name="operation",
                value_name="median_time_ms",
            )

            message_chart["operation"] = message_chart["operation"].map(
                {
                    "encryption_median_ms": "Encryption",
                    "decryption_median_ms": "Decryption",
                }
            )

            fig = px.line(
                message_chart,
                x="message_size_bytes",
                y="median_time_ms",
                color="operation",
                markers=True,
                title="Message size vs. median processing time",
                labels={
                    "message_size_bytes": "Message size (bytes)",
                    "median_time_ms": "Median time (ms)",
                    "operation": "Operation",
                },
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(message_df, use_container_width=True, hide_index=True)
        else:
            st.warning("The message benchmark CSV has an unexpected format.")

    if not file_df.empty:
        required = {
            "file_size_bytes",
            "encryption_median_ms",
            "decryption_median_ms",
            "encryption_throughput_mb_s",
            "decryption_throughput_mb_s",
        }

        if required.issubset(file_df.columns):
            st.markdown("### File encryption")

            file_chart = file_df.melt(
                id_vars=["file_size_bytes"],
                value_vars=[
                    "encryption_median_ms",
                    "decryption_median_ms",
                ],
                var_name="operation",
                value_name="median_time_ms",
            )

            file_chart["operation"] = file_chart["operation"].map(
                {
                    "encryption_median_ms": "Encryption",
                    "decryption_median_ms": "Decryption",
                }
            )

            fig = px.line(
                file_chart,
                x="file_size_bytes",
                y="median_time_ms",
                color="operation",
                markers=True,
                title="File size vs. median processing time",
                labels={
                    "file_size_bytes": "File size (bytes)",
                    "median_time_ms": "Median time (ms)",
                    "operation": "Operation",
                },
            )
            st.plotly_chart(fig, use_container_width=True)

            throughput_chart = file_df.melt(
                id_vars=["file_size_bytes"],
                value_vars=[
                    "encryption_throughput_mb_s",
                    "decryption_throughput_mb_s",
                ],
                var_name="operation",
                value_name="throughput_mb_s",
            )

            throughput_chart["operation"] = throughput_chart["operation"].map(
                {
                    "encryption_throughput_mb_s": "Encryption",
                    "decryption_throughput_mb_s": "Decryption",
                }
            )

            fig = px.line(
                throughput_chart,
                x="file_size_bytes",
                y="throughput_mb_s",
                color="operation",
                markers=True,
                title="File size vs. throughput",
                labels={
                    "file_size_bytes": "File size (bytes)",
                    "throughput_mb_s": "Throughput (MB/s)",
                    "operation": "Operation",
                },
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(file_df, use_container_width=True, hide_index=True)
        else:
            st.warning("The file benchmark CSV has an unexpected format.")

    st.caption(
        "Results depend on the machine, software environment, and benchmark "
        "configuration. They are measurements, not universal guarantees."
    )


if __name__ == "__main__":
    st.set_page_config(page_title="QuantumVault Performance", layout="wide")
    st.title("🔐 QuantumVault")
    render_performance_dashboard()
