#!/usr/bin/env python3

import argparse
import datetime
import logging

from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)


def date_str_to_week(date):
    """ Convert a YYYY-MM-DD date to YYYY-WEEKNR """
    year, month, day = map(int, date.split('-'))
    date = datetime.date(year, month, day)
    weeknr = date.isocalendar()[1]
    return f'{year}-{weeknr}'


def weekly_infections(fin):
    """ Determine the weekly infections """
    # Store the weekly 
    weekly = defaultdict(int)

    header = next(fin).strip().split(';')

    for line in fin:
        # Parse the line
        d = {k: v for k, v in zip(header, line.strip().split(';'))}
        
        # Add year-weeknr to the data (e.g. 2021-1)
        week = date_str_to_week(d['Date_of_publication'])

        # Add the infection count to the weekly dict
        weekly[week] += int(d['Total_reported'])

    return weekly


def weekly_variant_fraction(fin):
    """ Determine the fraction of each variant for each week """
    fractions = dict()

    header = next(fin).strip().split(';')

    for line in fin:
        # Parse the line
        d = {k: v for k, v in zip(header, line.strip().split(';'))}

        # We are only interested in named variants
        if not d['Variant_name']:
            continue

        # Make sure we do not include samples listed before
        assert d['May_include_samples_listed_before'] == 'False'

        # Determine the week number
        week = date_str_to_week(d['Date_of_statistics_week_start'])

        # Determine the fraction of the variant
        fraction = float(d['Variant_cases'])/float(d['Sample_size'])

        # If this is the first entry for this week, we have to create a dict to
        # store the results
        if week not in fractions:
            fractions[week] = {d['Variant_name']: fraction}
        else:
            fractions[week][d['Variant_name']] = fraction

    return fractions


def get_variants(fractions):
    """ Get the variant names from the fractions dict """
    for fraction in fractions.values():
        return sorted(fraction.keys())


def main(args):
    # Determine the weekly variant fractions
    with open(args.variants) as fin:
        variant_fractions = weekly_variant_fraction(fin)

    # Determine the weekly infections
    with open(args.daily_infections) as fin:
        weekly = weekly_infections(fin)

    # Print the weekly infections
    #print('Week', 'Count', sep=',')
    #for week, count in weekly.items():
    #    print(week, count, sep=',')

    # All variants
    variants = get_variants(variant_fractions)

    # Print the header
    print('Week', *variants, sep=',')

    # Print the data for each week
    for week, fractions in variant_fractions.items():
        # Get the variant names
        # Get the total number of infections
        infections = weekly[week]
        # Determine the weekly count for every variant
        values = [int(infections*fractions[name]) for name in variants]
        print(week, *values, sep=',')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--daily-infections', required=True)
    parser.add_argument('--variants', required=True)

    arguments = parser.parse_args()
    main(arguments)
