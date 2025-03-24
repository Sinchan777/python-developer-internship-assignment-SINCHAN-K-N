#Data collection

"""
Data will be collected using aviationstack api
Have taken reference airport or target airport i.e frankfurt airport
Timeout has been set to 10 seconds
logging has been implemented to easily get readable warnings along with exception handling"""

import sqlite3
import requests
import logging
import os 
from dotenv import load_dotenv

#logging configuration
logging.basicConfig(level=logging.INFO)

#Constants
API_URL = os.getenv('AVIATIONSTACK_URL')
API_KEY = os.getenv('AVIATIONSTACK_API_KEY')
DB_NAME = "airports.db"
TARGET_AIRPORT = "FRA"

#Defining function to fetch live data
def fetch_flights():
    try:
        response = requests.get(
            API_URL,
            params={
                "access_key": API_KEY,
                "dep_iata": TARGET_AIRPORT,
                "flight_status": "active"
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json().get('data', [])
    except Exception as e:
        logging.error(f"API Error: {e}")
        return []

#Save data to the database
def save_flights(flights):
    inserted = 0
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        for flight in flights:
            try:
                data = (
                    flight['flight']['iata'],
                    flight['departure']['iata'],
                    flight['arrival']['iata'],
                    flight['departure']['scheduled'],
                    flight['departure'].get('actual'),
                    flight['departure'].get('delay', 0),
                    flight['flight_status']
                )
            except KeyError as e:
                logging.warning(f"Missing field {e} in flight data")
                continue

            #Insert or ignore duplicates to handle missiong values
            cursor.execute('''
                INSERT OR IGNORE INTO flights
                (flight_number, departure_airport, arrival_airport,
                 scheduled_departure, actual_departure, delay_minutes, status)
                VALUES (?,?,?,?,?,?,?)
            ''', data)

            inserted += cursor.rowcount

        connection.commit()
        logging.info(f"Inserted {inserted} new flights")
        return inserted

    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return 0
    finally:
        if 'conn' in locals():
            connection.close()

if __name__ == "__main__":
    flights = fetch_flights()
    if flights:
        result = save_flights(flights)
        print(f"Flight data added : {result}")
    else:
        print("No flight data fetched")