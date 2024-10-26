import argparse


class FinanceCalculator:
    def __init__(self, revenue, costs):
        self.revenue = revenue
        self.costs = costs

    def profit(self):
        return self.revenue - self.costs

    def roi(self):
        return (self.profit() / self.costs) * 100


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--revenue', type=float, required=True, help='Укажите доходы компании: ')
    parser.add_argument('--costs', type=float, required=True, help='Укажите расходы компании: ')

    args = parser.parse_args()

    calculator = FinanceCalculator(args.revenue, args.costs)

    print(f'Чистая прибыль: {calculator.profit()} руб.')
    print(f'ROI: {calculator.roi():.2f}%')


if __name__ == '__main__':
    main()
