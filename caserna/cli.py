"""Console script for caserna."""
import argparse
import sys
from subprocess import PIPE, run
from caserna.weather_station.display import main as main_lcd
import os
from glog import GLog

logger = GLog('Caserna', {})

def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout

def check_process(script):
    """Check if a process is running"""
    script_name = script.replace('caserna -w ', '')
    process = str(out(f'ps -ax | grep -i "{script_name}" | grep -v -i "script_manager" | grep -v -i grep'))
    if not process:
        os.system(f'screen -dm -S "{script_name}" {script}')
    else:
        logger.info(f'{script_name} already running, exiting program...')
        exit()

def main():
    """Console script for caserna."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--weather', nargs='*')
    args = parser.parse_args()
    if args.weather:
        if args.weather[0] == 'activate':
            logger.info('Activate screen')
            check_process('caserna -w weather_station')
        elif args.weather[0] == 'weather_station':
            logger.info('Start weather station')
            main_lcd()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
