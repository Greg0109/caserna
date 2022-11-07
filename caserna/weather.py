import time
import os
from glog import GLog
HOSTNAME = os.uname()[1]
if HOSTNAME != 'caserna':
    from caserna.mocked_weather import Sensor, WindSpeedHistory, WindDirectionHistory, History
else:
    import weatherhat
    from weatherhat.history import (
        WindSpeedHistory,
        WindDirectionHistory,
        History
    )


LOGGER = GLog('weather', {})
SENSOR = Sensor() if os.uname()[1] != 'caserna' else weatherhat.WeatherHAT()
SENSOR_HISTORY = {
    'wind_speed': WindSpeedHistory(),
    'wind_direction': WindDirectionHistory(),
    'temperature': History(),
    'pressure': History(),
    'humidity': History(),
    'light': History(),
    'rain': History()
}

def get_sensor_data():
    """Get sensor data from WeatherHAT."""
    return {
        'wind_speed': SENSOR.wind_speed(),
        'wind_direction': SENSOR.wind_direction(),
        'temperature': SENSOR.temperature(),
        'pressure': SENSOR.pressure(),
        'humidity': SENSOR.humidity(),
        'light': SENSOR.light(),
        'rain': SENSOR.rain()
    }

def update_sensor_history():
    """Update sensor history."""
    data = get_sensor_data()
    for key, value in data.items():
        LOGGER.info(f'Updating {key} history with {value}')
        SENSOR_HISTORY[key].append(value)

def main():
    """Main function."""
    runs = 0
    while runs < 10:
        update_sensor_history()
        time.sleep(5)
        runs += 1
    print('\n')
    print('\n')
    for key, value in SENSOR_HISTORY.items():
        LOGGER.info(f'{key}: {value}')

if __name__ == "__main__":
    main()