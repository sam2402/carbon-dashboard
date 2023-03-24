import datetime
import atexit

from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from azure.mgmt.resource.resources.models import GenericResourceExpanded
from flask_cors import CORS 

from backend.future import predictions
import backend.carbon.azure_api as azure_api
import backend.carbon.electricity_mapper_api as em_api
import backend.advice.open_ai_api as open_ai_api
from backend.carbon.resource import resource_to_dict
from backend.carbon.sources.objs import location_zones
from backend.carbon.emissions import ResourceEmissionInfo
from backend.advice.advice_types import AdviceType
from backend.carbon.sources.objs import resource_metrics

app = Flask(__name__)
CORS(app)

azure_client: azure_api.AzureClient = azure_api.AzureClient()
em_client: em_api.ElectricityMapperClient = em_api.ElectricityMapperClient()
open_ai_client: open_ai_api.OpenAIClient = open_ai_api.OpenAIClient()

app.before_first_request(predictions.update_cache)
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(predictions.update_cache, 'interval', minutes=60)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

@app.route("/")
def start():
    """
    Should be called once server has started. It causes predictions.update_cache to be called
    Shows that the server is ready.

    Returns:
        dict: An empty dictionary.
    """
    print("SERVER READY!")
    return {"value": "SERVER READY!"}

@app.route("/resource-ids/<resourceGroup>")
def get_resource_ids(resourceGroup):
    """
    Retrieves the resource IDs for the given resource group.

    Args:
        resourceGroup (str): The name of the resource group.

    Returns:
        dict: A dictionary that contains a list of resource IDs.
    """
    resources = azure_client.get_resources_in_group(resourceGroup)
    return {
        "value": [resource.id for resource in resources]
    }

@app.route("/resources")
@app.route("/resources/<resourceGroup>")
def get_resources(resourceGroup: str=None):
    """
    Retrieves resources for a given resource group or all resource groups if not specified.
    Optionally filters resources by location.

    Args:
        resourceGroup (str, optional): The name of the resource group. Defaults to None.

    Returns:
        dict: A dictionary containing a list of resources as dictionaries.
    """
    location_param = request.args.get("location")
    if resourceGroup is not None:
        resources: list[GenericResourceExpanded] = azure_client.get_resources_in_group(resourceGroup)
    else:
        resource_groups: list[str] = azure_client.get_resource_groups()
        resources: list[GenericResourceExpanded] = []
        for resource_group in resource_groups:
            resources.extend(azure_client.get_resources_in_group(resource_group))
    
    if location_param is not None:
        resources = list(filter(lambda resource: resource.location==location_param, resources))

    return {
        "value": list(map(resource_to_dict, resources))
    }

@app.route("/locations")
@app.route("/locations/<resourceGroup>")
def get_locations(resourceGroup: str=None):
    """
    Retrieves the locations of resources in the specified resource group or all resource groups if None of the resource group is specified.

    Args:
        resourceGroup (str, optional): The name of the resource group. Defaults to None.

    Returns:
        dict: A dictionary that contains a list of resource locations.
    """
    if resourceGroup is not None:
        resources: list[GenericResourceExpanded] = azure_client.get_resources_in_group(resourceGroup)
    else:
        resource_groups: list[str] = azure_client.get_resource_groups()
        resources: list[GenericResourceExpanded] = []
        for resource_group in resource_groups:
            resources.extend(azure_client.get_resources_in_group(resource_group))
    
    locations = set(map(lambda resource: resource.location, resources))

    return {
        "value": sorted(list(locations))
    }

    
@app.route("/past-resource-emissions/<resourceGroup>")
@app.route("/past-resource-emissions/<resourceGroup>/<path:resourceId>")
def get_past_resource_emissions(resourceGroup: str, resourceId: str=None):
    """
    Retrieves the past carbon emissions data for a specific resource or for the entire resource group if None of the resource is specified.


    Args:
        resourceGroup (str): The name of the resource group.
        resourceId (str, optional): The ID of the specific resource. Defaults to None.

    Returns:
        dict: A dictionary containing a list of past carbon emissions data.
    """
    date_param = request.args.get("earliestDate")
    earliest_date = datetime.datetime.strptime(date_param, "%Y-%m-%d %H:%M:%S").date() if date_param else None
    interval = request.args.get("interval")
    if resourceId is not None:
        emissions = azure_client.get_emissions_for_resource(resourceGroup, "/"+resourceId, earliest_date, interval=interval)
    else:
        emissions = azure_client.get_emissions_for_resource_group(resourceGroup, earliest_date, interval=interval)

    return {
        "value": [
            {
                "date": emission["date"].isoformat(),
                "value": emission["value"],
            }
        for emission in emissions]
    }

@app.route("/past-total-emissions/<resourceGroup>")
@app.route("/past-total-emissions/<resourceGroup>/<path:resourceId>")
def get_past_total_emissions(resourceGroup: str, resourceId: str=None):
    """
    Retrieves the past total carbon emissions data for a specific resource or for the entire resource group if None of the resource is specified.

    Args:
        resourceGroup (str): The name of the resource group.
        resourceId (str, optional): The ID of the specific resource. Defaults to None.

    Returns:
        dict: A dictionary containing the total past carbon emissions.
    """
    date_param = request.args.get("earliestDate")
    earliest_date = datetime.datetime.strptime(date_param, "%Y-%m-%d %H:%M:%S").date() if date_param else None
    if resourceId is not None:
        emissions = azure_client.get_emissions_for_resource(resourceGroup, "/"+resourceId, earliest_date)
    else:
        emissions = azure_client.get_emissions_for_resource_group(resourceGroup, earliest_date)

    return {
        "value": round(sum(emission["value"] for emission in emissions))
    }

@app.route("/past-emissions-breakdown/<resourceGroup>")
def get_past_emissions_breakdown(resourceGroup: str):
    """
    Retrieves the past emissions breakdown information and location for a specific resource group.

    Args:
        resourceGroup (str): The name of the resource group.

    Returns:
        dict: A dictionary containing the past emissions breakdown information.
    """
    time = datetime.datetime.now()-datetime.timedelta(days=azure_api.METRICS_RETENTION_PERIOD)
    past_emissions_breakdown = {
        "renewablePercentage": None,
        "emissionsBreakdownDetail": {}
    }
    
    total_emissions = 0
    total_renewable_emissions = 0
    for resource in azure_client.get_resources_in_group(resourceGroup):
        emissions = azure_client.get_emissions_for_resource(resourceGroup, resource.id)
        total_resource_emissions = sum(emission["value"] for emission in emissions)
        total_emissions += total_resource_emissions
        lon, lat = location_zones[resource.location]["longitude"], location_zones[resource.location]["latitude"]
        detailed_power_consumption, _, renewable_percentage = em_client.get_power_consumption_breakdown(lon, lat, time)
        total_renewable_emissions += total_resource_emissions*(renewable_percentage/100)

        if resource.location not in past_emissions_breakdown["emissionsBreakdownDetail"]:
            past_emissions_breakdown["emissionsBreakdownDetail"][resource.location] = {}
        
        for power_type, power_percentage in detailed_power_consumption.items():
            if power_type not in past_emissions_breakdown["emissionsBreakdownDetail"][resource.location]:
                past_emissions_breakdown["emissionsBreakdownDetail"][resource.location][power_type] = 0
            past_emissions_breakdown["emissionsBreakdownDetail"][resource.location][power_type] += round(total_resource_emissions*(power_percentage/100), 1)

    past_emissions_breakdown["renewablePercentage"] = round((total_renewable_emissions/total_emissions)*100, 1)

    return {
        "value": past_emissions_breakdown
    }

@app.route("/current-emissions")
def get_current_emissions():
    """
    Retrieves the current carbon emissions data for a specific location.

    Returns:
        dict: A dictionary containing the current carbon emissions data.
    """
    location_param = request.args.get("location")
    if location_param is None:
        raise ValueError("Missing location parameter")

    resources = azure_client.get_resources_at_location(location_param)
    total_emissions = 0
    for resource_group, resources in resources.items():
        for resource in resources:
            res_ems = azure_client.get_emissions_for_resource(
                resource_group,
                resource.id,
                earliest_date=datetime.datetime.now()-datetime.timedelta(minutes=5),
                interval=resource_metrics[resource.type]["minInterval"]
            )
            total_emissions+= res_ems[-1]["value"] if res_ems else 0

    return {
        "value": {
            "location": location_param,
            "emissions": total_emissions
        }
    }

@app.route("/future-resource-emissions/<resourceGroup>")
@app.route("/future-resource-emissions/<resourceGroup>/<path:resourceId>")
def get_future_resource_emissions(resourceGroup: str, resourceId: str=None):
    """
    Retrieves the future carbon emissions data for a specific resource or for the entire resource group if None of the resource is specified.

    Args:
        resourceGroup (str): The name of the resource group.
        resourceId (str, optional): The ID of the specific resource. Defaults to None.

    Returns:
        dict: A dictionary containing a list of future carbon emissions data.
    """
    location_param = request.args.get("location")
    if resourceId is None and location_param is not None:
        emissions = predictions.get_location_prediction(location_param, resourceGroup)
    elif resourceId is None and resourceGroup is not None:
        emissions = predictions.get_resource_prediction(resourceGroup)
    elif resourceId is not None and resourceGroup is not None:
        emissions = predictions.get_resource_prediction(resourceGroup, resourceId)
    else:
        raise ValueError("You must specify a resourceGroup")
    
    return {
        "value": [
            {
                "date": emission["date"].isoformat(),
                "value": emission["value"],
            }
        for emission in emissions]
    }

@app.route("/advice")
def get_advice():
    """
        Retrieves advice for reducing emissions based on the given adviceType.

        Returns:
            dict: A dictionary containing advice on various aspects such as energy type, location, resource configuration and cooling type.
    """
    resource_group_param = request.args.get("resourceGroup")
    resource_id_param = request.args.get("resourceId")
    azure_location_param = request.args.get("azureLocation")
    advice_type_param = request.args.get("adviceType")
    matching_resources: dict[str, list[GenericResourceExpanded]] = {} # resource group: [resources]
    for resource_group in azure_client.get_resource_groups():
        if resource_group_param is None or resource_group_param == resource_group:
            matching_resources[resource_group] = []
            for resource in azure_client.get_resources_in_group(resource_group):
                if resource_id_param is None or resource_id_param == resource.id:
                    if azure_location_param is None or azure_location_param == resource.location:
                        matching_resources[resource_group].append(resource)

    resource_emission_infos = []
    for resource_group, resources in matching_resources.items():
        for resource in resources:
            one_week_ago = datetime.datetime.now()-datetime.timedelta(weeks=1)
            emissions = azure_client.get_emissions_for_resource(resource_group, resource.id, earliest_date=one_week_ago, interval="P1D")
            past_weeks_emissions = sum(data_point["value"] for data_point in emissions)
            lon, lat = location_zones[resource.location]["longitude"], location_zones[resource.location]["latitude"]
            power_consumption_breakdown, fossil_free_percentage, renewable_percentage = em_client.get_power_consumption_breakdown(lon, lat, datetime.datetime.now())
            resource_emission_infos.append(ResourceEmissionInfo(
                resource=resource,
                past_weeks_emissions=past_weeks_emissions,
                power_consumption_breakdown=power_consumption_breakdown,
                fossil_free_percentage=fossil_free_percentage,
                renewable_percentage=renewable_percentage
            ))
    
    advice = {}
    if advice_type_param is None or advice_type_param=="energyType":
        advice["energyType"] = open_ai_client.get_advice(resource_emission_infos, AdviceType.ENERGY_TYPE),
    if advice_type_param is None or advice_type_param=="location":
        advice["location"] = open_ai_client.get_advice(resource_emission_infos, AdviceType.LOCATION),
    if advice_type_param is None or advice_type_param=="resourceConfiguration":
        advice["resourceConfiguration"] = open_ai_client.get_advice(resource_emission_infos, AdviceType.RESOURCE_CONFIGURATION),
    if advice_type_param is None or advice_type_param=="coolingType":
        advice["coolingType"] = open_ai_client.get_advice(resource_emission_infos, AdviceType.COOLING_TYPE),
    

    return {
        "value": advice
    }

if __name__ == "__main__":
    """
    Starts the application and serves it on the default port.
    """
    app.run()
