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

def get_prompt(past_carbon_data: list[dict], resource: GenericResourceExpanded, power_consumption_breakdown: list, advice_type: AdviceType):
    prompt = ""

    latest_data = past_carbon_data[-1]
    current_carbon_emission = latest_data["value"]

    if advice_type == AdviceType.ENERGY_TYPE:
        prompt = f"Based on the current carbon emission of {current_carbon_emission}, please provide suggestions on how to improve energy types to reduce carbon emissions. Here is a summary of the power consumption breakdown for each zone:\n\n"
        for item in power_consumption_breakdown:
            zone = item['zone']
            breakdown = item['powerConsumptionBreakdown']
            breakdown_summary = ', '.join([f"{k}: {v}" for k, v in breakdown.items()])
            prompt += f"Zone {zone}: {breakdown_summary}\n"
    
    elif advice_type == AdviceType.LOCATION:
        location_name = resource.location
        lon, lat = location_zones[resource.location]["longitude"], location_zones[resource.location]["latitude"]
        prompt = f"With the resource located in {location_name} at longitude {lon} and latitude {lat} and a current carbon emission of {current_carbon_emission}, please provide suggestions on how to adjust the location to reduce carbon emissions."
   
    elif advice_type == AdviceType.RESOURCE_CONFIGURATION:
        cpu_tier = resource.sku["tier"] if resource.sku and "tier" in resource.sku else "default"
        cpu_model = cpus[cpu_tier]["model"]
        power_rating = cpus[cpu_tier]["power"]
        prompt = f"With the current resource configuration using a {cpu_model} CPU with a power rating of {power_rating} watts and a current carbon emission of {current_carbon_emission}, please provide suggestions on how to optimize the resource configuration to reduce carbon emissions."

    elif advice_type == AdviceType.RESOURCE_WORK_TIME:
        prompt = f"With the latest carbon emission data for the resource on {latest_data['date'].strftime('%Y-%m-%d')} having a value of {current_carbon_emission}, please provide suggestions on how to optimize the resource's work time to reduce carbon emissions."

    return prompt
