import argparse
from .financial_metrics import FinancialMetrics

def main():

    parser = argparse.ArgumentParser(description='Calculate financial metrics for a company.')
    parser.add_argument('--revenue', type=float, required=True, help='Specify the revenue of the company.')
    parser.add_argument('--costs', type=float, required=True, help='Specify the costs of the company.')

    args = parser.parse_args()
    metrics = FinancialMetrics(args.revenue, args.costs)

    print(f'Чистая прибыль: {metrics.net_profit()} руб.')
    print(f'ROI: {metrics.roi():.2f}%')

if __name__ == '__main__':
    main()
