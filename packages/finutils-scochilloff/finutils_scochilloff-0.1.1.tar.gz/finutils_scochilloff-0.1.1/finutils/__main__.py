import argparse
from .calculations import calculate_profit, calculate_roi


def main() -> None:
    parser = argparse.ArgumentParser(prog="finutils")
    parser.add_argument("--revenue", type=float, required=True)
    parser.add_argument("--costs", type=float, required=True)
    args = parser.parse_args()

    profit = calculate_profit(args.revenue, args.costs)
    roi = calculate_roi(args.revenue, args.costs)

    print(f"Чистая прибыль: {profit}\nROI: {roi}%")


if __name__ == "__main__":
    main()
