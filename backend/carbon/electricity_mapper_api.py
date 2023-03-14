import os
import datetime
import requests
from statistics import fmean

class ElectricityMapperClient:

    _instance = None
    
    def __init__(self):
        self.token = os.environ["ELECTRICITY_MAPPER_TOKEN"]
    
    "Implement ElectricityMapperClient as a Singleton"
    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(ElectricityMapperClient, cls).__new__(cls)
        return cls._instance
    
    def get_average_emissions(self, longitude: str, latitude: str, start_time: datetime.datetime, end_time: datetime.datetime) -> int:
        return 107
        duration = end_time - start_time
        if duration > datetime.timedelta(hours=2):
            mid_time = start_time + (end_time-start_time)/2
            return self._get_emissions_at_time(longitude, latitude, mid_time)
        else:
            return self._get_emissions_over_range(longitude, latitude, start_time, end_time)
    
    def _get_emissions_at_time(self, longitude: str, latitude: str, time: datetime.datetime) -> int:
        url = "https://api.electricitymap.org/v3/carbon-intensity/past"
        response = requests.get(
            url,
            params={
                "lon": longitude,
                "lat": latitude,
                "datetime": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
            headers={
                "auth-token": self.token,
            } 
        ).json()
        print(response)

        return response["carbonIntensity"]
    
    def _get_emissions_over_range(self, longitude: str, latitude: str, str, start_time: datetime.datetime, end_time: datetime.datetime) -> int:
        url = "https://api.electricitymap.org/v3/carbon-intensity/past-range"
        response = requests.get(
            url,
            params={
                "lon": longitude,
                "lat": latitude,
                "start": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "end": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
            headers={
                "auth-token": self.token,
            } 
        ).json()

        return fmean(snapshot["carbonIntensity"] for snapshot in response["data"])
        
