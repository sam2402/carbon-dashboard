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
    print("SERER READY!")
    return {}

@app.route("/resource-ids/<resourceGroup>")
def get_resource_ids(resourceGroup):
    resources = azure_client.get_resources_in_group(resourceGroup)
    return {
        "value": [resource.id for resource in resources]
    }

@app.route("/resources")
@app.route("/resources/<resourceGroup>")
def get_resources(resourceGroup: str=None):
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
    date_param = request.args.get("earliestDate")
    earliest_date = datetime.datetime.strptime(date_param, "%Y-%m-%d %H:%M:%S").date() if date_param else None
    if resourceId is not None:
        emissions = azure_client.get_emissions_for_resource(resourceGroup, "/"+resourceId, earliest_date)
    else:
        emissions = azure_client.get_emissions_for_resource_group(resourceGroup, earliest_date)

    return {
        "value": round(sum(emission["value"] for emission in emissions))
    }

@app.route("/future-resource-emissions/<resourceGroup>")
@app.route("/future-resource-emissions/<resourceGroup>/<path:resourceId>")
def get_future_resource_emissions(resourceGroup: str, resourceId: str=None):
    emissions = predictions.get_resource_prediction(resourceGroup) if resourceId is None else \
                predictions.get_resource_prediction(resourceGroup, resourceId)
    
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
    resource_group_param = request.args.get("resourceGroup")
    resource_id_param = request.args.get("resourceId")
    azure_location_param = request.args.get("azureLocation")
    advice_type_param = request.args.get("adviceType")
    print(advice_type_param)
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
        print("Hello")
        advice["energyType"] = open_ai_client.get_advice(resource_emission_infos, AdviceType.ENERGY_TYPE),
    if advice_type_param is None or advice_type_param=="location":
        advice["location"] = open_ai_client.get_advice(resource_emission_infos, AdviceType.LOCATION),
    if advice_type_param is None or advice_type_param=="resourceConfiguration":
        advice["resourceConfiguration"] = open_ai_client.get_advice(resource_emission_infos, AdviceType.RESOURCE_CONFIGURATION),
    if advice_type_param is None or advice_type_param=="coolingType":
        print("Hi")
        advice["coolingType"] = open_ai_client.get_advice(resource_emission_infos, AdviceType.COOLING_TYPE),
    

    return {
        "value": advice
    }

if __name__ == "__main__":
    app.run()

# http://127.0.0.1:5000/advice?resourceGroup=EmTech_RAE&resourceId=/subscriptions/59d64684-e7c9-4397-8982-6b775a473b74/resourceGroups/EmTech_RAE/providers/Microsoft.Web/staticSites/ava-emtech-rae
