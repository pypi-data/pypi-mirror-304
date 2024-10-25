import argparse
import sys
from .ec_metrics import net_profit, roi
def main():
    parser = argparse.ArgumentParser(description="Рассчитать чистую прибыль и ROI.")
    parser.add_argument('--revenue', type=float, required=True, help="Доходы компании")
    parser.add_argument('--costs', type=float, required=True, help="Затраты компании")
    args = parser.parse_args()
    revenue = args.revenue
    costs = args.costs
    profit = net_profit(revenue, costs)
    roi_value = roi(revenue, costs)
    print(f"Чистая прибыль: {profit:.2f} руб.")
    print(f"ROI: {roi_value:.2f}%")
if __name__ == '__main__':
    main()
