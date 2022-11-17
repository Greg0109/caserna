import time
import os
from glog import GLog
HOSTNAME = os.uname()[1]
if HOSTNAME != 'ega':
    from caserna.weather_station.mocked_weather import (
        Sensor,
        WindSpeedHistory,
        WindDirectionHistory,
        History
    )
    SENSOR = Sensor()
else:
    import weatherhat
    from weatherhat.history import (
        WindSpeedHistory,
        WindDirectionHistory,
        History
    )
    SENSOR = weatherhat.WeatherHAT()


LOGGER = GLog('weather', {})
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
        'wind_speed': SENSOR.wind_speed,
        'wind_direction': SENSOR.wind_direction,
        'temperature': SENSOR.temperature,
        'pressure': SENSOR.pressure,
        'humidity': SENSOR.humidity,
        'light': SENSOR.lux,
        'rain': SENSOR.rain
    }

def update_sensor_history():
    """Update sensor history."""
    data = get_sensor_data()
    for key, value in data.items():
        LOGGER.info(f'Updating {key} history with {value}')
        history = SENSOR_HISTORY[key]
        history.update(value)
    return SENSOR_HISTORY

def main():
    """Main function."""
    for _ in range(10):
        SENSOR.update(interval=1.0)
        print(update_sensor_history())
        time.sleep(5)
    print('\n')
    print('\n')
    for key, value in SENSOR_HISTORY.items():
        history = SENSOR_HISTORY[key]
        print(f'{key}: {history.get()}')

if __name__ == "__main__":
    main()