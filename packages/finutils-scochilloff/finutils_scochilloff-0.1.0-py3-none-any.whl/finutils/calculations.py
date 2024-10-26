def calculate_profit(revenue: float, costs: float) -> float:
    return revenue - costs


def calculate_roi(revenue: float, costs: float) -> float:
    profit = calculate_profit(revenue, costs)
    return (profit / costs) * 100