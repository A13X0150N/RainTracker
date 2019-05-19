#
#    Authors: Alex Olson, Sahana Srinivasa Reddy
#      Class: ECE 508 - Python Workshop
#       Date: Spring 2019
# Assignment: Final Project
#
# -----------------------------------------------------------------------------
#                              Rain Tracker
# -----------------------------------------------------------------------------
# This program tracks incoming rain for a user-selected area. The user enters
# a location to watch and RainTracker will tell them the probability of rain
# over the next 24 hours. It also looks at a 5-day forecasts to see if any
# storms are approaching the area. The application interacts with the user by
# through the use of a GUI.
#

# Libraries
from calendar import month_name
from collections import Counter
from datetime import datetime
import json
import re
import requests
# import tkinter as tk


# Cities being monitored for rain
class RainyCities:
    cities = []      # List of cities to watch
    filename = ''    # Filename of current cities to monitor
    x = {}           # Temporary storage of weather data
    __api_key = "d7884bd635ace15703ff6f28696291e5"   # API key for openweathermap.org [LIMIT 60 calls/hour]

    # Instantiate object from a file containing a list
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, 'r', encoding='utf-8') as file_object:
            self.cities = json.load(file_object)

    # Add a city to the list
    def add_city(self, city):
        print("\nAdding", city, "to the database")
        # First check if city is already on the list
        if city in self.cities:
            print("\n\t***", city, "is already in the database ***")
            return

        # Attempt a URL request
        self.__request_weather(city)

        # Check that the city was found
        if self.x["cod"] == "404":
            print("\n\t*** City not found ***")
            return
        else:
            self.cities.append(city)
            self.__update_file()

    # Remove a city from the list
    def remove_city(self, city):
        print("\nAttempting to remove", city, "from the database")
        try:
            self.cities.remove(city)
        except ValueError:
            print("\n\t***", city, "was not found in the database ***\n")
            return
        self.__update_file()

    # Check the weather forecast for any rain
    # *** List is every 3 hours, list[0] is most recent, list[39] is 5 days into future ***
    def check_weather(self, city_to_check):
        # Associated lists to gather rain statistics, if any
        rainy_month = []
        rainy_days = []
        rainy_hour = []

        # Get weather data for a particular city
        self.__request_weather(city_to_check)

        # Check for valid input
        try:
            weather_data = self.x["list"]
        except KeyError:
            print("\n\t*** City not found, check input ***")
            return

        # Parse out Month-Day-Hour data for any predicted rain
        for snapshot in weather_data:
            if snapshot['weather'][0]['main'] == "Rain":
                match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', snapshot['dt_txt'])
                date = datetime.strptime(match.group(), "%Y-%m-%d %H:%M:%S")
                rainy_month.append(date.month)
                rainy_days.append(date.day)
                rainy_hour.append(date.hour)
        print("\nRainy weather in", city_to_check, "over next 5 days:")
        if rainy_days:
            month = Counter(rainy_month).most_common()[0][0]
            day = Counter(rainy_days).most_common()[0][0]
            print("It will rain", len(set(rainy_days)), "out of 5 days")
            print("Rainiest day:   ", month_name[month], day)
            print("Rain frequency: ", len(rainy_days)*2.5, "%")
        else:
            print("No rain is forecasted for the next 5 days!")

    # Show current cities
    def print(self):
        print("\nCurrently monitoring the following cities:")
        for city in self.cities:
            print('\t-' + city)

    # [PRIVATE] Update .txt file with any new changes
    def __update_file(self):
        with open(self.filename, 'w', encoding='utf-8') as file_object:
            json.dump(self.cities, file_object)

    # [PRIVATE] Build a string for making a URL call
    def __build_url(self, city):
        base_url = "http://api.openweathermap.org/data/2.5/forecast?"
        complete_url = base_url + "appid=" + self.__api_key + "&q=" + city
        return complete_url

    # [PRIVATE] Request weather data
    def __request_weather(self, city):
        # Get weather data for a particular city
        url = self.__build_url(city)
        response = requests.get(url)
        self.x = response.json()


# Main application
def application_test():
    print("\n\n\tStarting RainTracker...\n\n")
    filename = "Cities.json"  # File for persistent data storage
    my_rainy_cities = RainyCities(filename)
    select = -1

    # Main menu
    while select != 0:
        print("\n\n\tMENU\n")
        print("0 Quit")
        print("1 Display application cities")
        print("2 Add a city")
        print("3 Remove a city")
        print("4 Show rain report")
        select = input("\nEnter a number and press enter: ")
        select = int(select)

        if select == 0:
            print("\n\tClosing application...\n\n")

        elif select == 1:
            my_rainy_cities.print()

        elif select == 2:
            to_add = input("Enter a city to add to the database: ")
            my_rainy_cities.add_city(to_add.capitalize())

        elif select == 3:
            to_remove = input("Enter a city to remove from the database: ")
            my_rainy_cities.remove_city(to_remove.capitalize())

        elif select == 4:
            to_check = input("Enter a city from the database: ")
            my_rainy_cities.check_weather(to_check.capitalize())

        else:
            print("\n\t *** Please enter a valid menu selection ***\n")


# Run the program   
application_test()
