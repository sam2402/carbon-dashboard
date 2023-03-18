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
    COOLING_TYPE = 4
    
def get_prompt(past_carbon_data: list[dict], resource: GenericResourceExpanded, power_consumption_breakdown: list, advice_type: AdviceType):
    prompt = ""

    latest_data = past_carbon_data[-1]
    current_carbon_emission = latest_data["value"]

    if advice_type == AdviceType.ENERGY_TYPE:
        prompt = f"Volvo have a server current carbon emission value is {current_carbon_emission}, please provide advice on how to change energy sources in order to decrease carbon emissions. Below is a list of each zone's breakdown of electricity use:\n"
        for item in power_consumption_breakdown:
            zone = item['zone']
            breakdown = item['powerConsumptionBreakdown']
            breakdown_summary = ', '.join([f"{k}: {v}" for k, v in breakdown.items()])
            prompt += f"Zone {zone}: {breakdown_summary}\n"
    
    elif advice_type == AdviceType.LOCATION:
        location_name = resource.location
        lon, lat = location_zones[resource.location]["longitude"], location_zones[resource.location]["latitude"]
        prompt = f"Volvo have a server is currently locted {location_name} at longitude {lon} and latitude {lat} and current carbon emission value is {current_carbon_emission}, could you please give some suggested location to move to then it can decrease carbon emissions."
   
    elif advice_type == AdviceType.RESOURCE_CONFIGURATION:
        cpu_tier = resource.sku["tier"] if resource.sku and "tier" in resource.sku else "default"
        cpu_model = cpus[cpu_tier]["model"]
        power_rating = cpus[cpu_tier]["power"]
        prompt = f"Volvo have a server is currently using a {cpu_model} CPU with a power rating of {power_rating} watts and current carbon emission value is {current_carbon_emission},  could you please give some exact suggested cpu type with lower power ratings but similar compatibility  to replace the current one then it can decrease carbon emissions."

    elif advice_type == AdviceType.COOLING_TYPE:
        prompt = f"Volvo have a server current carbon emission value is {current_carbon_emission}. Could you please suggest a suitable and efficient cooling type to the current server, along with an approximate cost estimation."

    return prompt
