"""This module is a mocked class for testing"""
import random

class Sensor():
    """Mocked sensor class"""
    def __init__(self, name='test'):
        self.name = name

    def wind_speed(self):
        """Mocked wind speed"""
        return random.randint(0, 100)

    def wind_direction(self):
        """Mocked wind direction"""
        return random.randint(0, 360)

    def temperature(self):
        """Mocked temperature"""
        return random.randint(0, 100)

    def pressure(self):
        """Mocked pressure"""
        return random.randint(0, 100)

    def humidity(self):
        """Mocked humidity"""
        return random.randint(0, 100)

    def light(self):
        """Mocked light"""
        return random.randint(0, 100)

    def rain(self):
        """Mocked rain"""
        return random.randint(0, 100)

def WindSpeedHistory():
    """Mocked wind speed history"""
    return []

def WindDirectionHistory():
    """Mocked wind direction history"""
    return []

def History():
    """Mocked history"""
    return []