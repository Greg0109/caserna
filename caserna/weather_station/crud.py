import psycopg2
from datetime import datetime

class PostgresCRUD:
    def __init__(self, host, database, user, password, port=5432):
        # Connect to the database
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )

        # Create a cursor
        self.cur = self.conn.cursor()

        # Create the tables if they don't already exist
        self.table_names = ['temperature', 'humidity', 'pressure', 'light', 'wind_speed', 'wind_direction', 'rain']
        for name in self.table_names:
            self.cur.execute(f"CREATE TABLE IF NOT EXISTS {name} (id SERIAL PRIMARY KEY, value REAL NOT NULL, timestamp TIMESTAMP NOT NULL)")
    
    def insert_record(self, table_name, value):
        # Insert a new record into a table
        timestamp = datetime.now()
        self.cur.execute(f"INSERT INTO {table_name} (value, timestamp) VALUES (%s, %s)", (value, timestamp))
        self.conn.commit()

    def update_record(self, table_name, record_id, value):
        # Update a record in a table
        self.cur.execute(f"UPDATE {table_name} SET value = %s WHERE id = %s", (value, record_id))
        self.conn.commit()

    def delete_record(self, table_name, record_id):
        # Delete a record from a table
        self.cur.execute(f"DELETE FROM {table_name} WHERE id = %s", (record_id,))
        self.conn.commit()

    def get_records(self, table_name):
        # Retrieve records from a table
        self.cur.execute(f"SELECT * FROM {table_name}")
        records = self.cur.fetchall()
        return records

    def close(self):
        # Close the cursor and connection
        self.cur.close()
        self.conn.close()
