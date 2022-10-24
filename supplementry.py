from pickle import load
from pandas import DataFrame
import requests
from requests import get
from math import radians

# https://api.ipgeolocation.io/astronomy?apiKey=API_KEY&location=New%20York,%20US
# https://pypi.org/project/geopy/
# https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}

with open('model_pickle', "rb") as f:
    imported_model = load(f)
with open('time_series_pickle', "rb") as ft:
    imported_time_series = load(ft)
KEYS = ["distance-to-solar-noon",
        "wind-direction",
        'wind-speed',
        'humidity',
        'average-pressure-(period)']
cols = ['dayofyear', 'dayofweek', 'quarter',
        'month', 'year', 'States', 'Regions']
STATE_MAPPER = {'andhra pradesh': 0,
                'arunachal pradesh': 1,
                'assam': 2,
                'bihar': 3,
                'chandigarh': 4,
                'chhattisgarh': 5,
                'dnh': 6,
                'delhi': 7,
                'goa': 8,
                'gujarat': 9,
                'hp': 10,
                'haryana': 11,
                'j&k': 12,
                'jharkhand': 13,
                'karnataka': 14,
                'kerala': 15,
                'mp': 16,
                'maharashtra': 17,
                'manipur': 18,
                'meghalaya': 19,
                'mizoram': 20,
                'nagaland': 21,
                'odisha': 22,
                'pondy': 23,
                'punjab': 24,
                'rajasthan': 25,
                'sikkim': 26,
                'tamil nadu': 27,
                'telangana': 28,
                'tripura': 29,
                'up': 30,
                'uttarakhand': 31,
                'west bengal': 32}

REGION_MAPPER = {'ER': 0, 'NER': 1, 'NR': 2, 'SR': 3, 'WR': 4}


def get_time_preds(dayofyear, dayofweek, quarter, month, year, States: str, Regions: str):
    return abs(float(imported_time_series.predict(
        DataFrame(
            list(zip([int(dayofyear)], [int(dayofweek)], [int(quarter)],
                     [int(month)], [int(year)],
                     [STATE_MAPPER.get(States.lower())], [REGION_MAPPER.get(Regions.upper())])),
            columns=cols)
    )[0]))

def get_preds(location):
    """Returns solar energy production estimates in watt

    Args:
        location (String): Location

    Returns:
        Float: Estimated solar energy prduced in watt
    """
    data = get_data(get_coordinates(location))
    return get_energy_preds(data[0], data[1], data[2], data[3], data[4])


def get_energy_preds(distance_to_solar_noon, wind_direction, wind_speed, humidity, average_pressure) -> float:
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
    return imported_model.predict(DataFrame(
        list(zip([distance_to_solar_noon], [wind_direction],
             [wind_speed], [humidity], [average_pressure])),
        columns=KEYS))[0]


def get_coordinates(location) -> list:
    """uses ipgeolocation api to find coordinates and solar noon and currenct time

    Args:
        location (String): Loction

    Returns:
        List[latitude, longitude, distance-tosolar-noon, current-time]
    """
    response = get(
        f"https://api.ipgeolocation.io/astronomy?apiKey=4c68beef16a44af1925b158adea34e8a&location={location}").json()
    return [response["location"]["latitude"], response["location"]["longitude"], response['solar_noon'], response["current_time"][:5]]


def get_data(info):
    """Get weather data from openweathermap

    Args:
        info (List[latitude, longitude, distance-tosolar-noon, current-time])

    Returns:
        List[distance from nsolar noon, wind direction, wind speed, pressure, humidity]
    """
    response = get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={info[0]}&lon={info[1]}&appid=57c061cb0881c2d71bf9c2275d883d28&units=metric")
    if response.status_code == 200:
        res = response.json()
        data = [time_diff(info[2].strip(":"), info[3].strip(":")), res["wind"]["deg"],
                res["wind"]["speed"], res['main']['pressure'], res['main']['humidity']]
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
