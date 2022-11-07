"""This module is a mocked class for testing"""
import random
import time

def get_current_time():
    """Mocked current time"""
    return time.time()

class Sensor():
    """Mocked sensor class"""
    def __init__(self, name='test'):
        self.name = name

    def wind_speed(self):
        """Mocked wind speed"""
        return {
            'speed': random.randint(0, 100),
            'time': get_current_time()
        }

    def wind_direction(self):
        """Mocked wind direction"""
        return {
            'direction': random.randint(0, 100),
            'time': get_current_time()
        }

    def temperature(self):
        """Mocked temperature"""
        return {
            'temperature': random.randint(0, 100),
            'time': get_current_time()
        }

    def pressure(self):
        """Mocked pressure"""
        return {
            'pressure': random.randint(0, 100),
            'time': get_current_time()
        }

    def humidity(self):
        """Mocked humidity"""
        return {
            'humidity': random.randint(0, 100),
            'time': get_current_time()
        }

    def light(self):
        """Mocked light"""
        return {
            'light': random.randint(0, 100),
            'time': get_current_time()
        }

    def rain(self):
        """Mocked rain"""
        return {
            'rain': random.randint(0, 100),
            'time': get_current_time()
        }

def WindSpeedHistory():
    """Mocked wind speed history"""
    return []

def WindDirectionHistory():
    """Mocked wind direction history"""
    return []

def History():
    """Mocked history"""
    return []