#!/usr/bib/env python3
"""
Script to test the database
"""
from caserna.constants import *
from caserna.weather_station.crud import PostgresCRUD
import random

TYPES_RECORD = [
    'temperature',
    'humidity',
    'pressure',
    'light',
    'wind_speed',
    'wind_direction',
    'rain'
]

def create_db_instance():
    """
    This method creates a PostgresCRUD instance
    """
    return PostgresCRUD(
        host='192.168.11.18',
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT
    )

def get_random_value():
    """
    This method returns a random value
    """
    return random.randint(0, 100)

def test_insert_record():
    """
    This method tests the insert_record method
    """
    crud = create_db_instance()
    crud.insert_record('temperature', get_random_value())
    records = crud.get_records('temperature')
    assert len(records) >= 1
    crud.close()

def test_insert_every_record():
    """
    This method tests the insert_record method
    """
    crud = create_db_instance()
    for record in TYPES_RECORD:
        crud.insert_record(record, get_random_value())
        records = crud.get_records(record)
        assert len(records) >= 1
    crud.close()

if __name__ == '__main__':
    test_insert_record()
    test_insert_every_record()