"""Console script for caserna."""
import argparse
import sys
from caserna.weather_station.weather import WeatherStation
from caserna.weather_station.flask_app import run


def main():
    """Console script for caserna."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--weather', nargs='*')
    args = parser.parse_args()
    if args.weather:
        if args.weather[0] == 'server':
            print('Running server')
            run()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
