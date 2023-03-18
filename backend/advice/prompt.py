from enum import Enum
from azure.mgmt.resource.resources.v2021_04_01.models import GenericResourceExpanded
import json

# Load cpu.json
with open("backend/carbon/sources/cpus.json", "r") as cpu_file:
    cpus = json.load(cpu_file)

# Load location_zone.json
with open("backend/carbon/sources/location_zones.json", "r") as location_zone_file:
    location_zones = json.load(location_zone_file)
    
class AdviceType(Enum):
    ENERGY_TYPE = 1
    LOCATION = 2
    RESOURCE_CONFIGURATION = 3
    RESOURCE_WORK_TIME = 4
    COOLING_TYPE = 5
    
def get_prompt(past_carbon_data: list[dict], resource: GenericResourceExpanded, power_consumption_breakdown: list, advice_type: AdviceType):
    prompt = ""

    latest_data = past_carbon_data[-1]
    current_carbon_emission = latest_data["value"]

    if advice_type == AdviceType.ENERGY_TYPE:
        prompt = f"The current carbon emission value: {current_carbon_emission}, please provide advice on how to change energy sources in order to decrease carbon emissions. Below is a list of each zone's breakdown of electricity use:\n"
        for item in power_consumption_breakdown:
            zone = item['zone']
            breakdown = item['powerConsumptionBreakdown']
            breakdown_summary = ', '.join([f"{k}: {v}" for k, v in breakdown.items()])
            prompt += f"Zone {zone}: {breakdown_summary}\n"
    
    elif advice_type == AdviceType.LOCATION:
        location_name = resource.location
        lon, lat = location_zones[resource.location]["longitude"], location_zones[resource.location]["latitude"]
        prompt = f"The current location of this resource is {location_name} at longitude {lon} and latitude {lat} and current carbon emission value is {current_carbon_emission}, please provide advice on how to change the location to decrease carbon emissions."
   
    elif advice_type == AdviceType.RESOURCE_CONFIGURATION:
        cpu_tier = resource.sku["tier"] if resource.sku and "tier" in resource.sku else "default"
        cpu_model = cpus[cpu_tier]["model"]
        power_rating = cpus[cpu_tier]["power"]
        prompt = f"The current resource configuration using a {cpu_model} CPU with a power rating of {power_rating} watts and current carbon emission value is {current_carbon_emission}, please provide advice on how to decrease carbon emissions by optimising the resource configuration."

    elif advice_type == AdviceType.RESOURCE_WORK_TIME:
        prompt = f"The latest carbon emission data for the resource on {latest_data['date'].strftime('%Y-%m-%d')} having a value of {current_carbon_emission}, please provide advice for how to optimize the resource's working hours to decrease carbon emissions."
        
    elif advice_type == AdviceType.COOLING_TYPE:
        prompt = f"The current carbon emission value is {current_carbon_emission}. Please provide advice on a suitable and efficient cooling type to replace the current one, along with an approximate cost estimation."

    return prompt
