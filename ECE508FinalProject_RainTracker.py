#
#    Authors: Alex Olson, Sahana Srinivasa Reddy
#      Class: ECE 508 - Python Workshop
#       Date: Spring 2019
# Assignment: Final Project
#
# -----------------------------------------------------------------------------
#                              RainTracker
# -----------------------------------------------------------------------------
# This program tracks incoming rain for a user-selected area. The user enters
# a location to watch and RainTracker will tell them the probability of rain
# over the next 24 hours. It also looks at 10-day forecasts to see if any 
# storms are approaching the area. The application interacts with the user by
# using a GUI. 
#

# Libraries
import tkinter as tk
import requests
import json

# Main application
def RainTracker():
    print("\n\n\tStarting RainTracker...\n\n")
    
    # Enter your API key here 
    api_key = "d7884bd635ace15703ff6f28696291e5"
      
    # base_url variable to store url 
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
      
    # Give city name 
    city_name = input("Enter city name : ") 
      
    # complete_url variable to store 
    # complete url address 
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
      
    # get method of requests module 
    # return response object 
    response = requests.get(complete_url)
    
    # json method of response object  
    # convert json format data into 
    # python format data 
    x = response.json()
    print(x)

    # Now x contains list of nested dictionaries 
    # Check the value of "cod" key is equal to 
    # "404", means city is found otherwise, 
    # city is not found 
    if x["cod"] != "404": 
      
        # store the value of "main" 
        # key in variable y 
        y = x["main"] 
      
        # store the value corresponding 
        # to the "temp" key of y 
        current_temperature = y["temp"] 
      
        # store the value corresponding 
        # to the "pressure" key of y 
        current_pressure = y["pressure"] 
      
        # store the value corresponding 
        # to the "humidity" key of y 
        current_humidiy = y["humidity"] 
      
        # store the value of "weather" 
        # key in variable z 
        z = x["weather"] 
      
        # store the value corresponding  
        # to the "description" key at  
        # the 0th index of z 
        weather_description = z[0]["description"] 
        
         # store the value corresponding  
        # to the "description" key at  
        # the 0th index of z 
        weather_description = z[0]["description"] 
      
        # print following values 
        print(" Temperature (in kelvin unit) = " +
                        str(current_temperature) + 
              "\n atmospheric pressure (in hPa unit) = " +
                        str(current_pressure) +
              "\n humidity (in percentage) = " +
                        str(current_humidiy) +
              "\n description = " +
                        str(weather_description)) 
  
    else: 
        print(" City Not Found ")
        
    
    print("\n\tClosing application...\n\n")

# Run the program   
RainTracker()
