#Data Insertion and Querying

"""Have to insert mock data for 5 German airports and 10 sample flights with a mix of
    on-time and delayed statuses.
    And for the next tasks i.e
      Retrieve all flights from a specific airport.
      Identify flights delayed by more than 2 hours.
      Fetch flight details using the flight number.
      there is a seperate file named "cli.py" which gives an interface
      with switch cases covering all the required queries
      """

import sqlite3
from datetime import datetime, timedelta #for storing date, time in datetime type and timedelta for calculating difference/deelays

#Defining function to data insertion
def insert_mock_data():
  connection = sqlite3.connect('airports.db')
  c = connection.cursor()

  #Lets insert 5 mock german airports
  german_airports = [('FRA', 'EDDF', 'Frankfurt Airport', 'Germany', 'Frankfurt', 50.0354, 8.5518),
                     ('MUC', 'EDDM', 'Munich Airport', 'Germany', 'Munich', 48.353889, 11.786111),
                     ('BER', 'EDDB', 'Berlin Brandenburg Airport', 'Germany', 'Berlin', 52.366667, 13.503333),
                     ('HAM', 'EDDH', 'Hamburg Airport', 'Germany', 'Hamburg', 53.630278, 9.988333),
                     ('CGN', 'EDDK', 'Cologne Bonn Airport', 'Germany', 'Cologne', 50.865833, 7.142778)]

  c.executemany("""INSERT INTO airports(
    iata_code, icao_code, airport_name, country, city, latitude, longitude
  )VALUES (?,?,?,?,?,?,?)""",german_airports)

  #lets insert 10 mock flights

  now = datetime.now()
  sample_flights = [
      ('LH438', 'FRA', 'JFK', now, now + timedelta(minutes=150), 150, 'delayed'),
      ('EW123', 'BER', 'CDG', now, now, 0, 'on-time'),
      ('AB456', 'MUC', 'HAM', now, now + timedelta(minutes=130), 130, 'delayed'),
      ('LH789', 'FRA', 'CGN', now, now, 0, 'on-time'),
      ('UX987', 'HAM', 'MAD', now, now + timedelta(minutes=90), 90, 'delayed'),
      ('EW654', 'BER', 'FRA', now, now + timedelta(minutes=60), 60, 'delayed'),
      ('LH321', 'CGN', 'MUC', now, now, 0, 'on-time'),
      ('AB135', 'MUC', 'FRA', now, now + timedelta(minutes=180), 180, 'delayed'),
      ('UX246', 'FRA', 'HAM', now, now, 0, 'on-time'),
      ('EW357', 'HAM', 'BER', now, now + timedelta(minutes=240), 240, 'delayed')
  ]

  c.executemany("""INSERT INTO flights
                        (flight_number, departure_airport, arrival_airport,
                          scheduled_departure, actual_departure, delay_minutes, status)
                        VALUES (?,?,?,?,?,?,?)""",sample_flights)
  connection.commit()
  connection.close()

if __name__ == "__main__":
  insert_mock_data()