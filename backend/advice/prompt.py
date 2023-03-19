from backend.advice.advice_types import AdviceType
from backend.carbon.emissions import ResourceEmissionInfo
from backend.carbon.sources.objs import cpus
    
def get_prompt(resource_emission_infos: list[ResourceEmissionInfo], advice_type: AdviceType) -> str:
    prompt = ""

    for resource_emission_info in resource_emission_infos:
        resource = resource_emission_info.resource
        current_carbon_emission = resource_emission_info.past_weeks_emissions
        power_consumption_breakdown = resource_emission_info.power_consumption_breakdown

        if advice_type == AdviceType.ENERGY_TYPE:
            prompt = f"Volvo have a server last week's carbon emission value is {current_carbon_emission}g, provide advice on how to change energy sources in order to decrease carbon emissions. Below is a list of each zone's breakdown of electricity usage by percentage:\n"
            breakdown_summary = ', '.join([f"{k}: {v}" for k, v in power_consumption_breakdown.items()])
            prompt += f"{breakdown_summary}\n"

        elif advice_type == AdviceType.LOCATION:
            location_name = resource.location
            prompt = f"Volvo have a server is currently located at {location_name} and last week's carbon emission value is {current_carbon_emission}g, give some suggested locations to in order to decrease carbon emissions.\n"

        elif advice_type == AdviceType.RESOURCE_CONFIGURATION:
            cpu_tier = resource.sku["tier"] if resource.sku and "tier" in resource.sku else "default"
            cpu_model = cpus[cpu_tier]["model"]
            power_rating = cpus[cpu_tier]["power"]
            prompt = f"Volvo have a server is currently using a {cpu_model} CPU with a power rating of {power_rating} watts and last week's carbon emission value is {current_carbon_emission}g, could you please give some exact suggested cpu type with lower power ratings but similar compatibility to replace the current one then it can decrease carbon emissions."

        elif advice_type == AdviceType.COOLING_TYPE:
            prompt = f"Volvo have a server last week's carbon emission value is {current_carbon_emission}g. Could you please suggest a suitable and efficient cooling type to the current server, along with an approximate cost estimation."

    return prompt