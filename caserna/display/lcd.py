#!/usr/bin/env python3

import ST7789
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import ManropeBold as UserFont
import time
import atexit

class Display():
    """
    This class handles the display where the weather data is shown.
    """
    
    def __init__(self):
        self.weather_data = {}
        self.spi_speed_mhz = 80
        self.display = ST7789.ST7789(
            rotation=90,
            port=0,
            cs=1,
            dc=9,
            backlight=13,
            spi_speed_hz=self.spi_speed_mhz * 1000 * 1000
        )
        self.display.begin()
        self.width = self.display.width
        self.height = self.display.height
        self.img, self.draw = self._create_canvas()
        self.font_size = 20
        self.font = ImageFont.truetype(UserFont, self.font_size)
        self.text_color = (255, 255, 255)
        self.back_color = (0, 170, 170)
        self.black_color = (0, 0, 0)
        self.type = 'Update'
        atexit.register(self.turn_off_display)

    def _create_canvas(self):
        """Create canvas to draw on."""
        img = Image.new('RGB', (self.width, self.height), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        return img, draw

    def _draw_weather_on_display(self):
        """Draw weather data on the display."""
        self._draw_type()
        self._draw_temperature()
        self._draw_humidity()
        self._draw_pressure()
        self._draw_wind_speed()
        self._draw_wind_direction()
        self._draw_rain()
        self._draw_light()

    def _draw_type(self):
        """Draw type on the display."""
        type_text = f'Type: {self.type}'
        self.draw.text((10, 215), type_text, font=self.font, fill=self.text_color)
        
    def _draw_temperature(self):
        """Draw temperature on the display."""
        temperature = self.weather_data['temperature']
        temperature_text = f'Temperature: {round(temperature, 2)}°C'
        self.draw.text((10, 5), temperature_text, font=self.font, fill=self.text_color)
    
    def _draw_humidity(self):
        """Draw humidity on the display."""
        humidity = self.weather_data['humidity']
        humidity_text = f'Humidity: {round(humidity, 2)}%'
        self.draw.text((10, 35), humidity_text, font=self.font, fill=self.text_color)

    def _draw_pressure(self):
        """Draw pressure on the display."""
        pressure = self.weather_data['pressure']
        pressure_text = f'Pressure: {round(pressure, 2)} hPa'
        self.draw.text((10, 65), pressure_text, font=self.font, fill=self.text_color)

    def _draw_wind_speed(self):
        """Draw wind speed on the display."""
        wind_speed = self.weather_data['wind_speed']
        wind_speed_text = f'Wind speed: {round(wind_speed, 2)} km/h'
        self.draw.text((10, 95), wind_speed_text, font=self.font, fill=self.text_color)

    def _draw_wind_direction(self):
        """Draw wind direction on the display."""
        wind_direction = self.weather_data['wind_direction']
        wind_direction_text = f'Wind direction: {round(wind_direction, 2)}'
        self.draw.text((10, 125), wind_direction_text, font=self.font, fill=self.text_color)

    def _draw_rain(self):
        """Draw rain on the display."""
        rain = self.weather_data['rain']
        rain_text = f'Rain: {round(rain, 2)} mm'
        self.draw.text((10, 155), rain_text, font=self.font, fill=self.text_color)

    def _draw_light(self):
        """Draw light on the display."""
        light = self.weather_data['light']
        light_text = f'Light: {round(light, 2)} lx'
        self.draw.text((10, 185), light_text, font=self.font, fill=self.text_color)

    def update_display(self, weather_data, type):
        """Update the display."""
        self._erase_display(self.back_color)
        self.type = type
        self.weather_data = weather_data
        self.draw.rectangle((0, 0, self.width, self.height), self.back_color)
        self._draw_weather_on_display()
        self.display.display(self.img)

    def _erase_display(self, color):
        """Erase the display."""
        self.draw.rectangle((0, 0, self.width, self.height), color)
        self.display.display(self.img)

    def turn_off_display(self):
        """Turn off the display."""
        self._erase_display(self.black_color)
        self.display.set_backlight(0)

def main():
    """Main function."""
    display = Display()
    while True:
        display.update_display(
            {
                "temperature": 20,
                "humidity": 50,
                "pressure": 1000,
                "wind_speed": 10,
                "wind_direction": "N",
                "rain": 0,
                "light": 100
            }
        )
        time.sleep(10)