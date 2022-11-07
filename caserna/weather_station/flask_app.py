"""This module creates a flask app"""
from flask import Flask
from caserna.weather_station.weather import get_sensor_data
from glog import GLog

app = Flask(__name__)
LOGGER = GLog('caserna_weather_server', {})

@app.route('/alive', methods=['GET'])
def alive():
    """Check if server is alive"""
    message = 'Server is alive'
    LOGGER.info(message)
    return message

@app.route('/weather_update', methods=['GET'])
def weather_update():
    data = get_sensor_data()
    LOGGER.info(f'Updating weather with {data}')
    return data

def run():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run()