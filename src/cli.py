###Data insertion and querying extended

"""
To showcase remaining 3 queries cli approach has been taken
User can simply select the query and data is fetched"""

import sqlite3

def execute_query(query, params=None):
    connection = sqlite3.connect('airports.db')
    c = connection.cursor()
    result = c.execute(query, params or ()).fetchall()
    connection.close()
    return result

def main_menu():
    print("\nData insertion remaining queries")
    print("1. Retrieve all flights from a specific airport")
    print("2. Identify flights delayed by more than 2 hours")
    print("3. Fetch flight details using the flight number")
    print("4. Exit")

def run_cli():
    while True:
        main_menu()
        choice = input("Enter choice: ")

        if choice == '1':
            iata = input("Enter departure airport IATA code: ").upper()
            results = execute_query('''SELECT * FROM flights
                                     WHERE departure_airport = ?''', (iata))

        elif choice == '2':
            results = execute_query('''SELECT * FROM flights
                                     WHERE delay_minutes > 120''')

        elif choice == '3':
            flight_num = input("Enter flight number: ").upper()
            results = execute_query('''SELECT * FROM flights
                                     WHERE flight_number = ?''', (flight_num))

        elif choice == '4':
            break

        print("\nResults:")
        for row in results:
            print(row)

if __name__ == "__main__":
    run_cli()