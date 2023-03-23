from dataclasses import dataclass
import datetime

from isodate import parse_duration
from azure.mgmt.resource.resources.models import GenericResource

from .sources.objs import resource_metrics, cpus, location_zones
from .electricity_mapper_api import ElectricityMapperClient

def get_carbon_coefficient(resource: GenericResource, carbon_per_kwh: int, interval: str) -> float:
    """
    Calculates the carbon coefficient with given resource based on type, carbon_per_kwh and a given interval.
    
    Args:
        resource (GenericResource): The resource informations which is calculated to the carbon coefficient. 
        carbon_per_kwh (int): The carbon emissions data per kilowatt-hour.
        interval (str): The time interval to be used for the calculation.

    Returns:
        float: The calculated carbon coefficient.
    """
    metric = resource_metrics[resource.type]

    cpu_power_rating: int = cpus[resource.sku.tier]["power"] if resource.sku and resource.sku.tier else cpus["default"]["power"]
    cpu_time_eq = get_cpu_time_eq(metric["name"], interval) # equivalent number of cpu seconds
    power_watts = cpu_power_rating * cpu_time_eq
    
    return power_watts/1000 * carbon_per_kwh

def get_cpu_time_eq(metric: str, interval: str) -> float:
    """
    Calculate the CPU time in seconds equivalent to the given metric and time interval.

    Args:
        metric (str): The resource usage metric which is get from Azure.
        interval (str): The time interval to be used for the calculation.

    Returns:
        float: The equivalent CPU time value as in seconds.
    """
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
    """
    Retrieves the carbon emissions per kilowatt-hour data for a given location and time range.

    Args:
        location (str): The location to be used for the calculation.
        start_time (datetime.datetime): The start time pint of the time range.
        end_time (str): The end time point of the time range.

    Returns:
        int: The carbon emissions data per kilowatt-hour for the specified location and time range.
    """

    lon, lat = location_zones[location]["longitude"], location_zones[location]["latitude"]
    return ElectricityMapperClient().get_average_emissions(lon, lat, start_time, end_time)
        
def duration_to_seconds(duration: str) -> int:
    """
    Converts the given duration string value to its equivalent number of seconds.

    Args:
        duration (str): The given duration string to used to wait for converting.

    Returns:
        int: The equivalent number of seconds.
    """

    return parse_duration(duration).total_seconds()

@dataclass
class ResourceEmissionInfo:
    """
    A data class that is created to represent the emission information of a specific resource.

    Attributes:
        resource (GenericResource): The resource for which the emission information is provided.
        past_weeks_emissions (int): The past week's total carbon emissions data for this specific resource.
        power_consumption_breakdown (dict): A dictionary containing the power consumption breakdown informations for that sepcific resource.
        fossil_free_percentage (int): The percentage of fossil-free energy used by the sepcific resource.
        renewable_percentage (int): The percentage of renewable energy used by the sepcific resource.
    """
    resource: GenericResource
    past_weeks_emissions: int
    power_consumption_breakdown: dict
    fossil_free_percentage: int
    renewable_percentage: int