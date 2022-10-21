import pickle
import pandas as pd
import requests
import time
from math import radians

# https://api.ipgeolocation.io/astronomy?apiKey=API_KEY&location=New%20York,%20US
# https://pypi.org/project/geopy/
# https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}

with open('model_pickle', "rb") as f:
    imported_model = pickle.load(f)
KEYS = ["distance-to-solar-noon", 
        "wind-direction",
        'wind-speed', 
        'humidity',
        'average-pressure-(period)']
    
def get_preds(location):
    """Returns solar energy production estimates in watt

    Args:
        location (String): Location

    Returns:
        Float: Estimated solar energy prduced in watt
    """
    data = get_data(get_coordinates(location))
    return get_energy_preds(data[0], data[1], data[2], data[3], data[4])

def get_energy_preds(distance_to_solar_noon, wind_direction, wind_speed, humidity, average_pressure):
    """Uses XG Booting to find solar Energy Generated

    Args:
        distance_to_solar_noon (Float): Distance from Solar noon in radians
        wind_direction (Float): wind direction in deg
        wind_speed (Float): Wind speed in m/s
        humidity (Float): humidity in %
        average_pressure (Float): avg pressure

    Returns:
        Float: Amount of electricity generated
    """
    return imported_model.predict(pd.DataFrame(
        list(zip([distance_to_solar_noon], [wind_direction], [wind_speed], [humidity], [average_pressure])), 
        columns=KEYS))[0]

def get_coordinates(location):
    """uses ipgeolocation api to find coordinates and solarr noon and currenct time

    Args:
        location (String): Loction

    Returns:
        List[latitude, longitude, distance-tosolar-noon, current-time]
    """
    response = requests.get(f"https://api.ipgeolocation.io/astronomy?apiKey=4c68beef16a44af1925b158adea34e8a&location={location}").json()
    return [response["location"]["latitude"], response["location"]["longitude"], response['solar_noon'], response["current_time"][:5]]


def get_data(info):
    """Get weather data from openweathermap

    Args:
        info (List[latitude, longitude, distance-tosolar-noon, current-time])

    Returns:
        List[distance from nsolar noon, wind direction, wind speed, pressure, humidity]
    """
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={info[0]}&lon={info[1]}&appid=57c061cb0881c2d71bf9c2275d883d28&units=metric")
    if response.status_code == 200:
        res = response.json()
        data = [time_diff(info[2].strip(":"), info[3].strip(":")), res["wind"]["deg"], res["wind"]["speed"], res['main']['pressure'], res['main']['humidity']]
        return data
    else:
        return response.status_code
            

def time_diff(t_noon, t_current):
    """Return time diff in rads

    Args:
        t_noon (time.struct_time): Solar Noon time
        t_current (time.struct_time): Current Time
    """
    return radians((((12 - float(t_current[0])) * 60) + (float(t_noon[1]) - float(t_current[1]))) / 60)
