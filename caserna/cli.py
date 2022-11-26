"""Console script for caserna."""
import argparse
import sys
from caserna.weather_station.weather import WeatherStation
from caserna.display.lcd import main as main_lcd
from caserna.display.buttons import Buttons
from caserna.weather_station.flask_app import run


def main():
    """Console script for caserna."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--weather', nargs='*')
    parser.add_argument('-d', '--display', nargs='*')
    args = parser.parse_args()
    if args.weather:
        if args.weather[0] == 'server':
            print('Running server')
            run()
    if args.display:
        if args.display[0] == 'test_lcd':
            print('Running LCD')
            main_lcd()
        elif args.display[0] == 'display_weather':
            print('Running buttons')
            Buttons()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
