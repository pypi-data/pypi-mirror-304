from argparse import ArgumentParser


def calculate_net_profit(revenue, costs):
    return revenue - costs


def calculate_roi(net_profit, costs):
    if costs == 0:
        return 0.
    return (net_profit / costs) * 100


def main():
    # парсер
    parser = ArgumentParser(
        description='Расчет чистой прибыли и ROI компании.')

    # аргументы
    parser.add_argument(
        '--revenue', type=float, required=True,
        help='Общие доходы компании.')
    parser.add_argument(
        '--costs', type=float, required=True,
        help='Общие затраты компании.')

    # парсинг аргументов
    args = parser.parse_args()

    # расчёт
    net_profit = calculate_net_profit(args.revenue, args.costs)
    roi = calculate_roi(net_profit, args.costs)

    # вывод
    print(f'Чистая прибыль: {net_profit:.2f} руб.')
    print(f'ROI: {roi:.2f}%')


if __name__ == '__main__':
    main()
