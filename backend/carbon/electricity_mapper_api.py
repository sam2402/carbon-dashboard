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
    Fossil_free_sources = ["nuclear", "geothermal", "biomass", "wind", "solar", "hydro", "hydro discharge", "battery discharge"]
    Renewable_sources = ["geothermal", "biomass", "wind", "solar", "hydro", "hydro discharge", "battery discharge"]
    
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
    def get_power_consumption_breakdown(self, longitude: str, latitude: str, time: datetime.datetime) -> tuple[dict, int, int]:
        """
        Dict of power types and percentage they contribute
        Fossil free percentage integer
        Renewable percentage integer
        """
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
        data = _get_power_consumption_breakdown_default() if "error" in response else response
        detailed_power_consumption = {power_type: round(value/data["powerConsumptionTotal"]*100, 1) for power_type, value in data["powerConsumptionBreakdown"].items()}
        return detailed_power_consumption, data["fossilFreePercentage"], data["renewablePercentage"]


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

def _get_power_consumption_breakdown_default():
        power_consumption_breakdown = {
            "nuclear": random.randint(0, 150),
            "geothermal": random.randint(0, 150),
            "biomass": random.randint(0, 150),
            "coal": random.randint(0, 150),
            "wind": random.randint(0, 150),
            "solar": random.randint(0, 150),
            "hydro": random.randint(0, 150),
            "gas": random.randint(0, 150),
            "oil": random.randint(0, 150),
            "unknown": random.randint(0, 10),
            "hydro discharge": random.randint(0, 150),
            "battery discharge": random.randint(0, 150),
        }
        total = sum(power_consumption_breakdown.values())

        return {  
            "powerConsumptionBreakdown": power_consumption_breakdown,
            "fossilFreePercentage": round((total/sum(power_consumption_breakdown[source] for source in ElectricityMapperClient.Fossil_free_sources))*100),
            "renewablePercentage": round((total/sum(power_consumption_breakdown[source] for source in ElectricityMapperClient.Renewable_sources))*100),
            "powerConsumptionTotal": total
        }
