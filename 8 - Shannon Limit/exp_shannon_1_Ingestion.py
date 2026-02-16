#!/usr/bin/env python3

"""

python "/Users/dswanagon/Relational Lysis Github/8 - Shannon Limit/exp_shannon_1_Ingestion.py" \
    --mode B \
    --chunk_mb 50 \
    --log mode_b_log.csv

RELATIONAL LYSIS — PHASE 1 INGESTION

Mode A:
    Raw data enters memory and is stored.

Mode B:
    Raw data NEVER enters memory.
    Only solved states (Diamond, Shadow) are stored.

Purpose:
Replicate Shannon-limit bypass behavior on 16 GB machine.
"""

import argparse
import time
import math
import csv
import os
import psutil


# ============================================================
# Deterministic Generator Parameters
# ============================================================

ALPHA = math.sqrt(2.0)
BETA = math.sqrt(3.0)


# ============================================================
# Raw Generator (MODE A ONLY)
# ============================================================

def generate_chunk(start_i, n):

    import numpy as np  # local import prevents accidental Mode B use

    i = np.arange(start_i, start_i + n, dtype=np.float64)
    return np.sin(ALPHA * i) + np.cos(BETA * i)


# ============================================================
# Solved State (RL compliant)
# ============================================================

def solved_state(start_i, n):

    # Diamond = deterministic generator law
    D = ("SIN_COS", ALPHA, BETA, start_i, n)

    # Shadow trace explicitly present (empty allowed)
    S = ()

    return (D, S)


# ============================================================
# Memory Monitor
# ============================================================

_proc = psutil.Process(os.getpid())

def rss_mb():
    return _proc.memory_info().rss / (1024 * 1024)


# ============================================================
# Experiment
# ============================================================

def run(mode, chunk_mb, logfile):

    floats_per_mb = (1024 * 1024) // 8
    chunk_len = chunk_mb * floats_per_mb

    store = []   # Mode A grows large; Mode B tiny
    start_index = 0
    chunk_index = 0
    cumulative_bytes = 0

    peak_rss = rss_mb()

    with open(logfile, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "mode",
            "chunk_index",
            "equivalent_bytes",
            "chunk_time_ms",
            "rss_mb",
            "peak_mb",
        ])

        try:

            while True:

                chunk_index += 1
                t0 = time.perf_counter()

                if mode == "A":

                    # Raw enters memory
                    x = generate_chunk(start_index, chunk_len)
                    store.append(x)

                else:

                    # RL Mode — raw never materialized
                    solved = solved_state(start_index, chunk_len)
                    store.append(solved)

                start_index += chunk_len
                cumulative_bytes += chunk_len * 8

                t1 = time.perf_counter()

                current = rss_mb()
                peak_rss = max(peak_rss, current)

                writer.writerow([
                    mode,
                    chunk_index,
                    cumulative_bytes,
                    (t1 - t0) * 1000.0,
                    f"{current:.3f}",
                    f"{peak_rss:.3f}",
                ])

                # ===== STREAM OUTPUT =====

                print(
                    f"Chunk {chunk_index:6d} | "
                    f"Downloaded MB={cumulative_bytes/1e6:10.1f} | "
                    f"RSS={current:8.1f} MB | "
                    f"Peak={peak_rss:8.1f} MB"
                )

        except MemoryError:
            print("\n*** MemoryError ***")

        except KeyboardInterrupt:
            print("\n*** Stopped by user ***")

    print("\nRun finished")
    print("Equivalent bytes:", cumulative_bytes)
    print("Peak RSS MB:", peak_rss)


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--mode", choices=["A", "B"], required=True)
    parser.add_argument("--chunk_mb", type=int, default=50)
    parser.add_argument("--log", required=True)

    args = parser.parse_args()

    print("\nRELATIONAL LYSIS — PHASE 1 INGESTION")
    print("Mode:", args.mode)
    print("Chunk MB:", args.chunk_mb)
    print("Log:", args.log)
    print()

    run(args.mode, args.chunk_mb, args.log)
