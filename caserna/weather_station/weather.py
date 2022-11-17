import time
from glog import GLog
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
    SENSOR.update(interval=1.0)
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
    SENSOR.update()
    data = get_sensor_data()
    for key, value in data.items():
        LOGGER.info(f'Updating {key} history with {value}')
        history = SENSOR_HISTORY[key]
        history.append(value)
    print('\n')

def main():
    """Main function."""
    for _ in range(10):
        update_sensor_history()
        time.sleep(5)
    print('\n')
    print('\n')
    for sensor_type, history in SENSOR_HISTORY.items():
        for item in history.history():
            print(f'{sensor_type}: {item.value} {item.timestamp}')
        
        print('\n')

if __name__ == "__main__":
    main()