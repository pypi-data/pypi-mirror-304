from . import roi, clear_profit
import argparse

def main(args):
    print(f'Чистая прибыль: {clear_profit(args.revenue, args.costs)} руб.')
    print(f'ROI: {roi(args.revenue, args.costs)}%')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--revenue', action='store')
    parser.add_argument('--costs', action='store')

    args = parser.parse_args()
    main(args)