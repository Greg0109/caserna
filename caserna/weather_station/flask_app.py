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
    LOGGER.info(f'Updating weather with {data}')
    # TODO fix TypeError: Object of type SensorHistory is not JSON serializable
    return data

def run():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run()