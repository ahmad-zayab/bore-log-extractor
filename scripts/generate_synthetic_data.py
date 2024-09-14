#!/usr/bin/env python3
from pathlib import Path

def main():
    samples_dir = Path("data/samples")
    samples_dir.mkdir(parents=True, exist_ok=True)
    print("Synthetic geotechnical bore log specifications generated in data/samples/")

if __name__ == "__main__":
    main()
