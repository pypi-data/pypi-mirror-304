import argparse
from package_1 import *

def main():
    parser = argparse.ArgumentParser(description='Calculate financial metrics.')
    parser.add_argument('--revenue', type=float, required=True, help='Revenue of the company')
    parser.add_argument('--costs', type=float, required=True, help='Costs of the company')
    args = parser.parse_args()

    net_profit = calculate_net_profit(args.revenue, args.costs)
    roi = calculate_roi(net_profit, args.costs)

    print(f'Чистая прибыль: {net_profit:.2f} руб.')
    print(f'ROI: {roi:.2f}%')

if __name__ == '__main__':
    main()