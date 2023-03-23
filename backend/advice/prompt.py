from backend.advice.advice_types import AdviceType
from backend.carbon.emissions import ResourceEmissionInfo
from backend.carbon.sources.objs import cpus, location_zones
    
def get_prompt(resource_emission_infos: list[ResourceEmissionInfo], advice_type: AdviceType) -> str:
    """
    Creates a prompt with server details and makes request for corresponding carbon emission reduce carbon emission advices based on the chosen advise type.    
    
    Args:
        resource_emission_infos(list[ResourceEmissionInfo]): A list of ResourceEmissionInfo objects containing server information.
        advice_type (AdviceType): An of the AdviceType enum which indicates the type of advice to generate.
    
    Returns:
        str: A formatted prompt containing server information and an specific type advice request.
    """
    
    intro = f"Here is some information about a few Volvo servers. Please provide specific suggestions on how to reduce carbon emissions for the following servers:\n\n"   
    server_info_prompts = []

    for resource_emission_info in resource_emission_infos:
        resource = resource_emission_info.resource
        resource_name = resource.name
        current_carbon_emission = resource_emission_info.past_weeks_emissions
        power_consumption_breakdown = resource_emission_info.power_consumption_breakdown

        if advice_type == AdviceType.ENERGY_TYPE:
            prompt = f"Volvo server {resource_name} has a carbon emission value of {current_carbon_emission}g from the last week. Below is a list of each zone's breakdown of electricity usage by percentage:\n"
            breakdown_summary = ', '.join([f"{k}: {v}" for k, v in power_consumption_breakdown.items()])
            prompt += f"{breakdown_summary}\n"

        elif advice_type == AdviceType.LOCATION:
            location_name = location_zones[resource.location]["name"]
            prompt = f"Volvo server {resource_name} is currently located at {location_name} and last week's carbon emission value is {current_carbon_emission}g.\n"

        elif advice_type == AdviceType.RESOURCE_CONFIGURATION:
            cpu_tier = resource.sku.tier if resource.sku is not None and resource.sku.tier is not None else "default"
            cpu_model = cpus[cpu_tier]["model"]
            power_rating = cpus[cpu_tier]["power"]
            prompt = f"Volvo server {resource_name} is currently using a {cpu_model} CPU with a power rating of {power_rating} watts and last week's carbon emission value is {current_carbon_emission}g.\n"

        elif advice_type == AdviceType.COOLING_TYPE:
            prompt = f"Volvo server {resource_name} has a carbon emission value of {current_carbon_emission}g from the last week.\n"

        server_info_prompts.append(prompt)
        
    if advice_type == AdviceType.ENERGY_TYPE:
        request_advice_prompt = "Provide advice on how to change energy sources for each server in order to decrease carbon emissions."
    elif advice_type == AdviceType.LOCATION:
        request_advice_prompt = "Give some suggested locations for each server in order to decrease carbon emissions."
    elif advice_type == AdviceType.RESOURCE_CONFIGURATION:
        request_advice_prompt = "Could you please give some exact suggested cpu types with lower power ratings but similar compatibility to replace the current one for each server then it can decrease carbon emissions."
    elif advice_type == AdviceType.COOLING_TYPE:
        request_advice_prompt = "Could you please suggest a suitable and efficient cooling type for each server, along with an approximate cost estimation."

    return intro + "\n".join(server_info_prompts) + request_advice_prompt
