#!/usr/bin/env python3
"""MiniMart API pipeline: lint -> test -> build -> deploy.

Cara pakai:
    python pipeline.py --stages lint,test
    python pipeline.py --stages deploy
"""

import argparse
import os
import subprocess
import sys


def run(cmd):
    print(f"+ {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, check=True)


def stage_lint(ctx):
    # syntax check semua file Python (tanpa dependency tambahan)
    run([sys.executable, "-m", "compileall", "-q", "app", "tests"])


def stage_test(ctx):
    run([sys.executable, "-m", "pytest", "-v"])


def stage_build(ctx):
    # placeholder sampai Fase 3 (Docker). Pipeline tetap jalan.
    print("build: skip (Dockerfile belum ada, baru di Fase 3)")


def stage_deploy(ctx):
    host = os.environ["VPS_HOST"]
    user = os.environ.get("VPS_USER", "deploy")
    key = os.environ.get("SSH_KEY_PATH", os.path.expanduser("~/.ssh/id_ed25519"))
    run(
        [
            "ssh",
            "-i",
            key,
            "-o",
            "StrictHostKeyChecking=accept-new",
            f"{user}@{host}",
            "/home/deploy/minimart-api/deploy.sh",
        ]
    )


STAGES = {
    "lint": stage_lint,
    "test": stage_test,
    "build": stage_build,
    "deploy": stage_deploy,
}


def main():
    parser = argparse.ArgumentParser(description="MiniMart API pipeline")
    parser.add_argument(
        "--stages",
        default=",".join(STAGES),
        help=f"tahap yang dijalankan, dipisah koma (pilihan: {', '.join(STAGES)})",
    )
    args = parser.parse_args()

    ctx = {}
    for name in args.stages.split(","):
        name = name.strip()
        if name not in STAGES:
            print(f"ERROR: stage '{name}' tidak dikenal. Pilihan: {', '.join(STAGES)}")
            sys.exit(2)
        print(f"\n=== stage: {name} ===", flush=True)
        STAGES[name](ctx)
    print("\nPipeline OK")


if __name__ == "__main__":
    main()
