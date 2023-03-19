from backend.advice.advice_types import AdviceType
from backend.carbon.emissions import ResourceEmissionInfo
from backend.carbon.sources.objs import cpus, location_zones
    
def get_prompt(resource_emission_infos: list[ResourceEmissionInfo], advice_type: AdviceType) -> str:
    prompts = []

    for resource_emission_info in resource_emission_infos:
        resource = resource_emission_info.resource
        resource_id = resource.id
        current_carbon_emission = resource_emission_info.past_weeks_emissions
        power_consumption_breakdown = resource_emission_info.power_consumption_breakdown

        if advice_type == AdviceType.ENERGY_TYPE:
            prompt = f"Volvo server {resource_id} has a carbon emission value of {current_carbon_emission}g from the last week, provide advice on how to change energy sources in order to decrease carbon emissions. Below is a list of each zone's breakdown of electricity usage by percentage:\n"
            breakdown_summary = ', '.join([f"{k}: {v}" for k, v in power_consumption_breakdown.items()])
            prompt += f"{breakdown_summary}\n"

        elif advice_type == AdviceType.LOCATION:
            location_name = location_zones[resource.location]["name"]
            prompt = f"Volvo server {resource_id} is currently located at {location_name} and last week's carbon emission value is {current_carbon_emission}g, give some suggested locations in order to decrease carbon emissions.\n"

        elif advice_type == AdviceType.RESOURCE_CONFIGURATION:
            cpu_tier = resource.sku.tier if resource.sku is not None and resource.sku.tier is not None else "default"
            cpu_model = cpus[cpu_tier]["model"]
            power_rating = cpus[cpu_tier]["power"]
            prompt = f"Volvo server {resource_id} is currently using a {cpu_model} CPU with a power rating of {power_rating} watts and last week's carbon emission value is {current_carbon_emission}g, could you please give some exact suggested cpu types with lower power ratings but similar compatibility to replace the current one then it can decrease carbon emissions.\n"

        elif advice_type == AdviceType.COOLING_TYPE:
            prompt = f"Volvo server {resource_id} has a carbon emission value of {current_carbon_emission}g from the last week. Could you please suggest a suitable and efficient cooling type for the current server, along with an approximate cost estimation.\n"

        prompts.append(prompt)

    return "\n".join(prompts)
