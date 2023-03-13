from azure.mgmt.resource.resources.models import GenericResource
import datetime

def get_carbon_coefficient(resource: GenericResource, time: datetime.datetime):
    power_kwh = 5
    carbon_per_kwh = 6
    return power_kwh * carbon_per_kwh
