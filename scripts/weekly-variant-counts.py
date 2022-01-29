#!/usr/bin/env python3

import argparse
import datetime
import logging

from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)


def weekly_infections(fin):
    """ Determine the weekly infections """
    # Store the weekly 
    weekly = defaultdict(int)

    header = next(fin).strip().split(';')

    for line in fin:
        # Parse the line
        d = {k: v for k, v in zip(header, line.strip().split(';'))}
        
        # Add year-weeknr to the data (e.g. 2021-1)
        year, month, day = map(int, d['Date_of_publication'].split('-'))
        date = datetime.date(year, month, day)
        weeknr = date.isocalendar()[1]
        week = f'{year}-{weeknr}'

        # Add the infection count to the weekly dict
        weekly[week] += int(d['Total_reported'])

    return weekly


def main(args):
    with open(args.daily_infections) as fin:
        weekly = weekly_infections(fin)

    # Print the weekly infections
    print('Week', 'Count', sep=',')
    for week, count in weekly.items():
        print(week, count, sep=',')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--daily-infections', required=True)
    parser.add_argument('--variants', required=True)

    arguments = parser.parse_args()
    main(arguments)
