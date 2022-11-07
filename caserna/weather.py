import time
import weatherhat
from weatherhat.history import WindSpeedHistory

sensor = weatherhat.WeatherHAT()
wind_speed_history = WindSpeedHistory()

while True:
    sensor.update(interval=5.0)
    if sensor.updated_wind_rain:
        wind_speed_history.append(sensor.wind_speed)
        print(f"Average wind speed: {wind_speed_history.average_mph()}mph")
        print(f"Wind gust: {wind_speed_history.gust_mph()}mph")
    time.sleep(1.0)