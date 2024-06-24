"""
Upload data to databse using crud
"""
from caserna.constants import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER
)
from caserna.weather_station.crud import PostgresCRUD

class DBUpload():
    """
    This class is used to upload data to Database
    """

    def __init__(self):
        self.crud = None


    def connect_db(self):
        """
        This method connects to the postgres db
        """
        self.crud = PostgresCRUD(
            host=POSTGRES_HOST,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            port=POSTGRES_PORT
        )

    def upload_to_db(self, data):
        """
        This method uploads the data to the database
        """
        self.connect_db()
        print("Uploading data to database")
        for key, value in data.items():
            print(f"{key}: {value}")
            self.crud.insert_record(key, value)
        print("Data uploaded to database")
