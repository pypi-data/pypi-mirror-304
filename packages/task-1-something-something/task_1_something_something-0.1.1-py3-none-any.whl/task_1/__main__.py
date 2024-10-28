import task_1

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--revenue', type=int, required=True)
parser.add_argument('--costs', type=int, required=True)

args = parser.parse_args()

print(f'Чистая прибыль: {task_1.get_revenue(args.revenue, args.costs)} руб.',
      f'ROI: {task_1.get_roi(task_1.get_revenue(args.revenue, args.costs), args.costs)}%', sep='\n')
