import datetime
import atexit

from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler

from backend.future import predictions
import backend.carbon.azure_api as azure_api
from backend.carbon.resource import resource_to_dict


app = Flask(__name__)
azure_client: azure_api.AzureClient = azure_api.AzureClient()

app.before_first_request(predictions.update_cache)
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(predictions.update_cache, 'interval', minutes=60)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

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
                "date": emission["date"].strftime("%Y-%m-%d %H:%M:%S"),
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
        "value": sum(emission["value"] for emission in emissions)
    }

@app.route("/future-resource-emissions/<resourceGroup>")
@app.route("/future-resource-emissions/<resourceGroup>/<path:resourceId>")
def get_future_resource_emissions(resourceGroup: str, resourceId: str=None):
    if resourceId is None:
        return predictions.get_resource_prediction(resourceGroup)
    return predictions.get_resource_prediction(resourceGroup, resourceId)

# @app.route("/advice")
# def get_advice():
#     resource_group_param = request.args.get("resourceGroup")
#     resource_id_param = request.args.get("resourceId")
#     azure_location_param = request.args.get("azureLocation")
#     matching_resources = {} # resource group: [resources]
#     for resource_group in azure_client.get_resource_groups():
#         if resource_group_param is None or resource_group_param == resource_group:
#             resource_group[resource_group] = []
#             for resource in azure_client.get_resources_in_group(resource_group):
#                 if resource_id_param or resource_id_param == resource.id:
#                     if azure_location_param is None or azure_location_param == resource.location:
#                         matching_resources.append(resource)
    
    
#     for resource_group in matching_resources:
        


#     resource_emissions = [{
#         resource.id: {
#             "total_emissions":  azure_client.get_emissions_for_resource(
#                 res, "/"+resourceId, earliest_date
#             )
#         }
#     } for resource in matching_resources]


if __name__ == "__main__":
    app.run()
