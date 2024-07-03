"""
Scheduler & Console for Caserna
"""
import argparse
import sys
from fan import main as main_fan
from caserna.weather_station.display import main as main_lcd


def main():
    """Console script for caserna."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--weather', nargs='*')
    args = parser.parse_args()
    if args.weather:
        if args.weather[0] == 'weather_station':
            print('Start weather station')
            main_lcd()
        if args.weather[0] == 'fan':
            print('Start fan')
            main_fan()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
