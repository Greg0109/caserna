"""Console script for caserna."""
import argparse
import sys
from caserna.weather import main as weather_main


def main():
    """Console script for caserna."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'weather', help='Run weather script'
    )
    args = parser.parse_args()
    if args.weather:
        weather_main()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
