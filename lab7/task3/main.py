from __future__ import annotations

from pathlib import Path


def main() -> None:
    print("Task 3")
    print("======")
    print("This folder is prepared for the neural network experiment.")
    print("The dataset and model are not chosen yet.")
    print("Fill in dataset loading, train/test split, baseline optimizer and custom optimizer here.")
    print(f"Working directory: {Path(__file__).resolve().parent}")


if __name__ == "__main__":
    main()
