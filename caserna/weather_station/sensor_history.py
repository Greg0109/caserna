import datetime

class SensorHistory():
    """Sensor history."""
    def __init__(self, sensor_type):
        self.sensor_type = sensor_type
        self.history = []

    def add(self, value):
        """Add value to history."""
        if isinstance(value, float):
            value = round(value, 2)
        elif isinstance(value, str):
            raise ValueError('Cannot add string to history.')

        new_entry = {
            'value': value,
            'timestamp': datetime.datetime.now()
        }
        self.history.append(new_entry)

    def get_history(self):
        """Get history."""
        return self.history

    def get_highest_value(self):
        """Get highest value."""
        highest_value = 0
        for item in self.history:
            if item['value'] > highest_value:
                highest_value = item['value']
        return highest_value

    def get_lowest_value(self):
        """Get lowest value."""
        lowest_value = 0
        for item in self.history:
            if item['value'] < lowest_value:
                lowest_value = item['value']
        return lowest_value

    def get_average_value(self):
        """Get average value."""
        total = sum(item['value'] for item in self.history)
        return total / len(self.history)

    


def sensor_history_dictionary():
    return {
        'wind_speed': SensorHistory('wind_speed'),
        'wind_direction': SensorHistory('wind_direction'),
        'temperature': SensorHistory('temperature'),
        'pressure': SensorHistory('pressure'),
        'humidity': SensorHistory('humidity'),
        'light': SensorHistory('light'),
        'rain': SensorHistory('rain')
    }
