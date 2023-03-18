import os
import datetime
import random
import requests
from statistics import fmean
import functools

def date_range(start: datetime.datetime, end: datetime.datetime, delta: datetime.timedelta, pairs=False):
    time = start
    while time < end:
        next_time = min(time + delta, end)
        yield (time, next_time) if pairs else time
        time = next_time


class ElectricityMapperClient:

    _instance = None
    
    def __init__(self):
        self.token = os.environ["ELECTRICITY_MAPPER_TOKEN"]
    
    # Implement ElectricityMapperClient as a Singleton"
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ElectricityMapperClient, cls).__new__(cls)
        return cls._instance
    
    @functools.cache
    def get_emissions_over_time(self, longitude: str, latitude: str, start_time: datetime.datetime, end_time: datetime.datetime):
        """
        Return a dictionary of hour by hour emissions
        """
        emissions_by_hour = {}
        for start, end in date_range(start_time, end_time, datetime.timedelta(days=9), pairs=True):
            emissions = self._get_emissions_over_range(longitude, latitude, start, end)
            for data_point in emissions:
                emission_time = datetime.datetime.strptime(data_point["datetime"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(minute=0, second=0, microsecond=0)
                emissions_by_hour[emission_time] = data_point["carbonIntensity"]

        return emissions_by_hour
    
    @functools.cache
    def get_average_emissions(self, longitude: str, latitude: str, start_time: datetime.datetime, end_time: datetime.datetime) -> int:
        duration = end_time - start_time
        if duration > datetime.timedelta(hours=2):
            mid_time = start_time + (end_time-start_time)/2
            return self._get_emissions_at_time(longitude, latitude, mid_time)
        else:
            return self._get_emissions_average(longitude, latitude, start_time, end_time)
    
    @functools.cache
    def get_power_consumption_breakdown(self, longitude: str, latitude: str, time: datetime.datetime) -> list:
        url = "https://api.electricitymap.org/v3/power-breakdown/past-range"
        response: dict = requests.get(
            url,
            params={
                "lon": longitude,
                "lat": latitude,
                "datetime": time.isoformat(),
            },
            headers={
                "auth-token": self.token,
            } 
        ).json()
        
        return response.get("data", power_consumption_breakdown_default)
    
    @functools.cache
    def _get_emissions_at_time(self, longitude: str, latitude: str, time: datetime.datetime) -> int:
        url = "https://api.electricitymap.org/v3/carbon-intensity/past"
        response = requests.get(
            url,
            params={
                "lon": longitude,
                "lat": latitude,
                "datetime": time.isoformat(),
            },
            headers={
                "auth-token": self.token,
            } 
        ).json()

        return _get_emissions_at_time_default(time) if "error" in response else response["carbonIntensity"]
    
    @functools.cache
    def _get_emissions_average(self, longitude: str, latitude: str, start_time: datetime.datetime, end_time: datetime.datetime) -> int:        
        data_points = self._get_emissions_over_range(longitude, latitude, start_time, end_time)
        return fmean(data_point["carbonIntensity"] for data_point in data_points)
    
    @functools.cache
    def _get_emissions_over_range(self, longitude: str, latitude: str, start_time: datetime.datetime, end_time: datetime.datetime) -> list:
        url = "https://api.electricitymap.org/v3/carbon-intensity/past-range"
        response = requests.get(
            url,
            params={
                "lon": longitude,
                "lat": latitude,
                "start": start_time.isoformat(),
                "end": end_time.isoformat()
            },
            headers={
                "auth-token": self.token,
            } 
        ).json()
        
        return response.get("data", _get_emissions_over_range_default(start_time, end_time)["data"])


# Defaults used here as Avanade's Electricity Mapper key does not support the required regions
power_consumption_breakdown_default = {
    "data": [
        {
        "zone": "DK-DK1",
        "datetime": "2020-01-04T00:00:00.000Z",
        "updatedAt": "2022-04-07T09:35:03.914Z",
        "createdAt": "2022-02-04T15:49:58.284Z",
        "powerConsumptionBreakdown": {
            "nuclear": 65,
            "geothermal": 0,
            "biomass": 188,
            "coal": 195,
            "wind": 1642,
            "solar": 0,
            "hydro": 13,
            "gas": 72,
            "oil": 8,
            "unknown": 5,
            "hydro discharge": 0,
            "battery discharge": 0
        },
        "powerProductionBreakdown": {
            "nuclear": None,
            "geothermal": None,
            "biomass": 319,
            "coal": 287,
            "wind": 3088,
            "solar": 0,
            "hydro": 2,
            "gas": 97,
            "oil": 10,
            "unknown": 3,
            "hydro discharge": None,
            "battery discharge": None
        },
        "powerImportBreakdown": {
            "DE": 1070,
            "NL": 0,
            "SE": 0,
            "DK-DK2": 0,
            "NO-NO2": 0
        },
        "powerExportBreakdown": {
            "DE": 0,
            "NL": 700,
            "SE": 12,
            "DK-DK2": 589,
            "NO-NO2": 1387
        },
        "fossilFreePercentage": 87,
        "renewablePercentage": 84,
        "powerConsumptionTotal": 2189,
        "powerProductionTotal": 3806,
        "powerImportTotal": 1070,
        "powerExportTotal": 2687,
        "isEstimated": False,
        "estimationMethod": None
        }
    ]
}

def _get_emissions_at_time_default(time):
    return {
        "zone": "DE",
        "carbonIntensity": random.randint(100, 400),
        "datetime": time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z",
        "updatedAt": time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z",
        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z",
        "emissionFactorType": "lifecycle",
        "isEstimated": False,
        "estimationMethod": None
    }

def _get_emissions_over_range_default(start_time, end_time):
    return {
        "data": [
            _get_emissions_at_time_default(time)
            for time in date_range(start_time, end_time, datetime.timedelta(hours=1))
        ]
    }