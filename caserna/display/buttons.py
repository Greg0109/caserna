import signal
import RPi.GPIO as GPIO
from caserna.display.lcd import Display
import requests
import time
import os

class Buttons():
    """
    This class handles the action for the buttons
    """

    def __init__(self):
        self.buttons = [5, 6, 16, 24]
        self.labels = ['A', 'B', 'X', 'Y']
        self.server_url = "http://localhost:5000/"
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buttons, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.display = Display()
        self.weather_retrieval_types = {
            'update': 'weather_update',
            'average': 'weather_average',
            'max': 'weather_max',
            'off': 'weather_off'
        }
        self.weather_type = 'update'
        self.timer = 10
        self.attach_buttons()
        self.get_weather_and_display()

    def _get_weather(self):
        """Get weather data from the server."""
        response = requests.get(self.server_url + self.weather_retrieval_types[self.weather_type])
        return response.json()

    def handle_button(self, pin):
        """Handle button press."""
        label = self.labels[self.buttons.index(pin)]

        if label == 'A':
            self.weather_type = 'update'
        elif label == 'B':
            self.weather_type = 'average'
        elif label == 'X':
            self.weather_type = 'off'
        elif label == 'Y':
            self.weather_type = 'shutdown'

        if self.weather_type == 'shutdown':
            self.shutdown()
        elif self.weather_type == 'off':
            self.display.turn_off_display()
        else:
            weather_data = self._get_weather()
            self.display.update_display(weather_data, self.weather_type)

    def shutdown(self):
        """Shutdown the display."""
        self.display.turn_off_display()
        GPIO.cleanup()
        os.system("sudo shutdown -h now")

    def attach_buttons(self):
        """Attach buttons to the handle_button function."""
        for pin in self.buttons:
            GPIO.add_event_detect(pin, GPIO.FALLING, self.handle_button, bouncetime=100)

    def get_weather_and_display(self):
        """Get weather data and display it."""
        while True:
            if self.weather_type != 'off':
                weather_data = self._get_weather()
                self.display.update_display(weather_data, self.weather_type)
                time.sleep(self.timer)
            else:
                self.display.turn_off_display()
                time.sleep(1)
