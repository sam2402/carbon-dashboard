import datetime
import types
import json

from flask import Flask, g, request
from flask_api import status

import backend.carbon.azure_api as azure_api
from backend.carbon.resource import resource_to_dict


app = Flask(__name__)
azure_client: azure_api.AzureClient = azure_api.AzureClient()

@app.route("/resource-ids/<resourceGroup>")
def get_resource_ids(resourceGroup):
    resources = azure_client.get_resources_in_group(resourceGroup)
    return {
        "value": [resource.id for resource in resources]
    }

@app.route("/resources/<resourceGroup>")
def get_resources(resourceGroup):
    country = request.args.get("country")
    continent = request.args.get('continent')
    resources = azure_client.get_resources_in_group(resourceGroup)
    return {
        "value": list(map(resource_to_dict, resources))
    }
    
@app.route("/past-resource-emissions/<resourceGroup>")
@app.route("/past-resource-emissions/<resourceGroup>/<resourceId>")
def get_past_resource_emissions(resourceGroup: str, resourceId: str=None):
    date_param = request.args.get("earliestDate")
    earliest_date = datetime.datetime.strptime(date_param, '%Y-%m-%d').date() if date_param else None
    interval = request.args.get("interval")
    if resourceId:
        emissions = azure_client.get_emissions_for_resource(resourceGroup, resourceId, earliest_date, interval)
    emissions = azure_client.get_emissions_for_resource_group(resourceGroup, earliest_date, interval)
    return {
        "value": [
            {
                "date": emission["date"].strftime('%Y-%m-%d'),
                "value": emission["value"],
            }
        for emission in emissions]
    }

@app.route("/past-total-emissions/<resourceGroup>")
@app.route("/past-total-emissions/<resourceGroup>/<resourceId>")
def get_past_total_emissions(resourceGroup: str, resourceId: str=None):
    date_param = request.args.get("earliestDate")
    earliest_date = datetime.datetime.strptime(date_param, '%Y-%m-%d').date() if date_param else None
    if resourceId:
        emissions = azure_client.get_emissions_for_resource(resourceGroup, resourceId, earliest_date)
    emissions = azure_client.get_emissions_for_resource_group(resourceGroup, earliest_date)

    return {
        "value": sum(emission["value"] for emission in emissions)
    }

@app.route("/commuter-emissions")
def get_commuter_emissions():
    resourceId = request.args.get('resourceId')
    use_equivalent = request.args.get('useEquivalent')

if __name__ == "__main__":
    app.run()
