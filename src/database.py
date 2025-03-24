### Airport database creation
"""
Task is to create a detailed database of all European airports with :
  Airport name
  IATA code
  ICAO code
  Country
  City
  Latitude and Longitude
"""

#I understand that this is an internship for
#python developer position hence I will be using sqlite3
#sqlite is lightweight and self contained and whatever databases are present
#it will be stored in a single file

import sqlite3

#Defining a function to create datbase
def create_database():
  connection = sqlite3.connect('airports.db')
  c = connection.cursor()#airports.db will be created and cursor is defined

  c.execute("""
    CREATE TABLE IF NOT EXISTS airports (
        iata_code TEXT PRIMARY KEY,
        icao_code TEXT UNIQUE NOT NULL,
        airport_name TEXT NOT NULL,
        country TEXT NOT NULL,
        city TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL
    );""")#airports table

  #Will be utilsing Aviationstack API which provides
  #aviation data, including real-time flight status,
  #historical flights, schedules, airline routes, airports, aircrafts, and more.

  #So we will create a table called flights which stores data provided by aviationstack

  c.execute("""
  CREATE TABLE IF NOT EXISTS flights(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_number TEXT NOT NULL,
    departure_airport TEXT,
    arrival_airport TEXT,
    scheduled_departure DATETIME,
    actual_departure DATETIME,
    delay_minutes INTEGER DEFAULT 0,
    status TEXT CHECK(status IN ('on-time', 'delayed', 'cancelled')),
    FOREIGN KEY(departure_airport) REFERENCES airports(iata_code),
    FOREIGN KEY(arrival_airport) REFERENCES airports(iata_code)
  );""")

  connection.commit()
  connection.close()

if __name__ == "__main__":
  create_database()