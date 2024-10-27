import sys
from logging import exception

from .utils import *
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--revenue",
        type=float
    )
    parser.add_argument(
        "--costs",
        type=float
    )

    args = parser.parse_args()
    if not (args.revenue, args.costs):
        print("Недостаточно данных")
        sys.exit(1)
    try:
        print(f"Чистая прибыль: {income(args.revenue, args.costs)}")
        print(f'ROI: {roi(args.revenue, args.costs)}')
    except exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()