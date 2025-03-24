import sqlite3
import requests
from datetime import datetime
import os

#Configuration
DATABASE = "airports.db"
API_KEY = os.getenv('AVIATIONSTACK_API_KEY')
TARGET_AIRPORT = "FRA"

#data collection and processing
def main():
    try:
        #Fetch live flight data
        print("Fetching flight data...")
        response = requests.get(
            "http://api.aviationstack.com/v1/flights",
            params={
                "access_key": API_KEY,
                "dep_iata": TARGET_AIRPORT,
                "flight_status": "active"
            }
        )
        response.raise_for_status()
        flights = response.json().get('data', [])

        if not flights:
            print("No flight data received")
            return

        #Connect to database
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        #Process and store data
        new_flights = 0
        for flight in flights:
            try:
                #Extract essential fields
                flight_data = (
                    flight['flight']['iata'],
                    flight['departure']['iata'],
                    flight['arrival']['iata'],
                    flight['departure']['scheduled'],
                    flight['departure'].get('actual'),
                    flight['departure'].get('delay', 0),
                    flight['flight_status']
                )

                #Insert or ignore duplicates
                cursor.execute('''
                    INSERT OR IGNORE INTO flights
                    (flight_number, departure_airport, arrival_airport,
                     scheduled_departure, actual_departure, delay_minutes, status)
                    VALUES (?,?,?,?,?,?,?)
                ''', flight_data)

                new_flights += cursor.rowcount

            except KeyError as e:
                print(f"Skipping incomplete flight data: {e}")
                continue

        #Commiting changes and showing results
        connection.commit()
        print(f"Successfully stored {new_flights} new flights")

        #Show delayed flights
        delayed = cursor.execute('''
            SELECT flight_number, delay_minutes
            FROM flights
            WHERE delay_minutes > 120
        ''').fetchall()

        print("\nDelayed flights:")
        for flight, delay in delayed:
            print(f"{flight}: {delay} minutes delay")

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        if 'conn' in locals():
            connection.close()

if __name__ == "__main__":
    main()