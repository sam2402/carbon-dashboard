import datetime

from isodate import parse_duration
from azure.mgmt.resource.resources.models import GenericResource

from .sources.objs import resource_metrics, cpus, location_zones
from .electricity_mapper_api import ElectricityMapperClient

def get_carbon_coefficient(resource: GenericResource, carbon_per_kwh: int, interval: str) -> float:
    metric = resource_metrics[resource.type]

    cpu_power_rating: int = cpus[resource.sku.tier]["power"] if resource.sku and resource.sku.tier else cpus["default"]["power"]
    cpu_time_eq = get_cpu_time_eq(metric["name"], interval) # equivalent number of cpu seconds
    power_watts = cpu_power_rating * cpu_time_eq
    
    return power_watts/1000 * carbon_per_kwh

def get_cpu_time_eq(metric: str, interval: str) -> float:
    if metric in ["cpu_percent", "CpuPercentage"]:
        return duration_to_seconds(interval)
    elif metric in ["Usage", "Transactions", "SiteHits"]:
        # usage is the number of api calls made
        # assume each api call has 100% CPU utilization for 100ms
        return 0.1
    elif metric == "CpuTime":
        return 1
    raise KeyError(f"Unsupported metric: {metric}")

def get_carbon_emissions_per_kwh(location: str, start_time: datetime.datetime, end_time: str) -> int:
    lon, lat = location_zones[location]["longitude"], location_zones[location]["latitude"]
    return ElectricityMapperClient().get_average_emissions(lon, lat, start_time, end_time)
        
def duration_to_seconds(duration: str) -> int:
    return parse_duration(duration).total_seconds()