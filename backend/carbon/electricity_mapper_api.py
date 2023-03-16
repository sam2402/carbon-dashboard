import os
import datetime
import requests
from statistics import fmean

class ElectricityMapperClient:

    _instance = None
    
    def __init__(self):
        self.token = os.environ["ELECTRICITY_MAPPER_TOKEN"]
    
    # Implement ElectricityMapperClient as a Singleton"
    def __new__(cls):
        if cls._instance is None:
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
    
    def get_power_consumption_breakdown(self, longitude: str, latitude: str, time: datetime.datetime) -> list:
        return [
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
            "estimationMethod": False
            }
        ]
        url = "https://api.electricitymap.org/v3/power-breakdown/past-range"
        return requests.get(
            url,
            params={
                "lon": longitude,
                "lat": latitude,
                "datetime": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
            headers={
                "auth-token": self.token,
            } 
        ).json()["data"]
    
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
        
