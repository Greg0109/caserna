import time
from glog import GLog
import weatherhat
from caserna.weather_station.sensor_history import sensor_history_dictionary

class WeatherStation():
    """The weather station."""
    def __init__(self):
        self.sensor = weatherhat.WeatherHAT()
        self.logger = GLog('Weather', {})
        self.sensor_history = sensor_history_dictionary()

    def get_sensor_data(self):
        """Get sensor data from WeatherHAT."""
        self.sensor.update(interval=1.0)
        return {
            'wind_speed': self.sensor.wind_speed,
            'wind_direction': self.sensor.wind_direction,
            'temperature': self.sensor.temperature,
            'pressure': self.sensor.pressure,
            'humidity': self.sensor.humidity,
            'light': self.sensor.lux,
            'rain': self.sensor.rain
        }

    def update_sensor_history(self):
        """Update sensor history."""
        self.sensor.update()
        data = self.get_sensor_data()
        for key, value in data.items():
            self.logger.info(f'Updating {key} history with {value}')
            history = self.sensor_history[key]
            history.add(value)
        return self.sensor_history

    def test_function(self):
        """Main function."""
        for _ in range(10):
            self.update_sensor_history()
            time.sleep(5)
        print('\n')
        print('\n')
        for sensor_type, history in self.sensor_history.items():
            for item in history.get_history():
                for value, timestamp in item.items():
                    print(f'{sensor_type}: {value} - {timestamp}')
            print('\n')
