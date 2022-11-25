"""This module creates a flask app"""
from flask import Flask
from caserna.weather_station.weather import WeatherStation
import json
from glog import GLog

app = Flask(__name__)
WEATHER_STATION = WeatherStation()
LOGGER = GLog('caserna_weather_server', {})

@app.route('/', methods=['GET'])
def alive():
    """Check if server is alive"""
    message = 'Server is alive'
    LOGGER.info(message)
    return message

@app.route('/weather_update', methods=['GET'])
def weather_update():
    data = WEATHER_STATION.update_sensor_history()
    data_json = {
        'wind_speed': data['wind_speed'].get_latest_value(),
        'wind_direction': data['wind_direction'].get_latest_value(),
        'temperature': data['temperature'].get_latest_value(),
        'pressure': data['pressure'].get_latest_value(),
        'humidity': data['humidity'].get_latest_value(),
        'light': data['light'].get_latest_value(),
        'rain': data['rain'].get_latest_value()
    }
    for sensor, data in data_json.items():
        LOGGER.info(f'{sensor}: {data}')
    return data_json

@app.route('/weather_history', methods=['GET'])
def weather_history():
    data = WEATHER_STATION.update_sensor_history()
    data_json = {
        'wind_speed': data['wind_speed'].get_history(),
        'wind_direction': data['wind_direction'].get_history(),
        'temperature': data['temperature'].get_history(),
        'pressure': data['pressure'].get_history(),
        'humidity': data['humidity'].get_history(),
        'light': data['light'].get_history(),
        'rain': data['rain'].get_history()
    }
    for sensor, data in data_json.items():
        LOGGER.info(f'{sensor}: {data}')
    return data_json

def run():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run()