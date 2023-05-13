from Adafruit_IO import Client, Feed, Dashboard, RequestError
from glog import GLog
from caserna.constants import *
from caserna.weather_station.crud import PostgresCRUD

ADAFRUIT_IO_KEY = 'aio_ywME22AR8MY156ONa8NESVronCNz'
ADAFRUIT_IO_USERNAME = 'GRabago'

class AdafruitUpload():
    """
    This class is used to upload data to Adafruit IO
    """

    def __init__(self):
        self.temperature_feed = None
        self.humidity_feed = None
        self.pressure_feed = None
        self.light_feed = None
        self.windspeed_feed = None
        self.winddirection_feed = None
        self.rain_feed = None
        self.dashboard = None
        self.logger = GLog('AdafruitUpload', {
            'write_to_file': True,
            'send_errors': True,
            'file_name': 'adafruit_upload.log',
            'file_path': '/home/pi/Desktop/'
        })
        try:
            self.aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
            self.create_dashboard()
            self.create_and_assing_feeds()
            self.crud = PostgresCRUD(
                host=POSTGRES_HOST,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                port=POSTGRES_PORT
            )
        except RequestError as error:
            self.logger.error(error)

    def create_and_assing_feeds(self):
        """
        This method creates the feeds and assigns them to the dashboard
        """
        # Create new feeds
        try:
            self.aio.create_feed(Feed(name="Temperature"))
            self.aio.create_feed(Feed(name="Relative Humidity"))
            self.aio.create_feed(Feed(name="Pressure"))
            self.aio.create_feed(Feed(name="Light"))
            self.aio.create_feed(Feed(name="Wind Speed"))
            self.aio.create_feed(Feed(name="Wind Direction"))
            self.aio.create_feed(Feed(name="Rain"))
            self.logger.info("Feeds created!")
        except RequestError:
            self.logger.info("Feeds already exist!")

        self.temperature_feed = self.aio.feeds('temperature')
        self.humidity_feed = self.aio.feeds('relative-humidity')
        self.pressure_feed = self.aio.feeds('pressure')
        self.light_feed = self.aio.feeds('light')
        self.windspeed_feed = self.aio.feeds('wind-speed')
        self.winddirection_feed = self.aio.feeds('wind-direction')
        self.rain_feed = self.aio.feeds('rain')

    def create_dashboard(self):
        """
        This method creates the dashboard
        """
        # Create new dashboard
        try:
            self.dashboard = self.aio.create_dashboard(Dashboard(name="Weather Dashboard"))
            self.logger.info("Dashboard created!")
        except RequestError:
            self.logger.info("Dashboard already exists!")

        self.dashboard = self.aio.dashboards('weather-dashboard')

    def upload_to_db(self, data):
        """
        This method uploads the data to the database
        """
        for key, value in data.items():
            self.logger.info(f"{key}: {value}")
            self.crud.insert_record(key, value)
        self.logger.info("Data uploaded to database")

    def upload_data(self, data):
        """
        This method uploads the data to Adafruit IO
        """
        try:
            self.aio.send_data(self.temperature_feed.key, data['temperature'])
            self.aio.send_data(self.humidity_feed.key, data['humidity'])
            self.aio.send_data(self.pressure_feed.key, data['pressure'])
            self.aio.send_data(self.light_feed.key, data['light'])
            self.aio.send_data(self.windspeed_feed.key, data['wind_speed'])
            self.aio.send_data(self.winddirection_feed.key, data['wind_direction'])
            self.aio.send_data(self.rain_feed.key, data['rain'])
            self.logger.info("Data uploaded to Adafruit IO")
        except RequestError as error:
            self.logger.error(error)
        finally:
            self.upload_to_db(data)

    def erase_all_data_from_feeds(self):
        """
        This method erases all data from the feeds
        """
        temperature_data = self.aio.data(self.temperature_feed.key)
        for data in temperature_data:
            self.aio.delete(self.temperature_feed.key, data.id)
        humidity_data = self.aio.data(self.humidity_feed.key)
        for data in humidity_data:
            self.aio.delete(self.humidity_feed.key, data.id)
        pressure_data = self.aio.data(self.pressure_feed.key)
        for data in pressure_data:
            self.aio.delete(self.pressure_feed.key, data.id)
        light_data = self.aio.data(self.light_feed.key)
        for data in light_data:
            self.aio.delete(self.light_feed.key, data.id)
        windspeed_data = self.aio.data(self.windspeed_feed.key)
        for data in windspeed_data:
            self.aio.delete(self.windspeed_feed.key, data.id)
        winddirection_data = self.aio.data(self.winddirection_feed.key)
        for data in winddirection_data:
            self.aio.delete(self.winddirection_feed.key, data.id)
        rain_data = self.aio.data(self.rain_feed.key)
        for data in rain_data:
            self.aio.delete(self.rain_feed.key, data.id)
