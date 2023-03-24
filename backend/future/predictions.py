import datetime

from azure.mgmt.resource.resources.models import GenericResourceExpanded

from ..carbon.azure_api import AzureClient
from .Model import get_future_emissions

Prediction = list[dict[str, str | float]]

predictions_cache: dict[str, dict[str, Prediction]] = {}
_az_client: AzureClient = AzureClient()

def update_cache():
    """
    Update the most recent information for each resource group and resource to the predictions cache.

    """
    now = datetime.datetime.now()
    for resource_group in _az_client.get_resource_groups():
        if resource_group not in predictions_cache:
            predictions_cache[resource_group] = {}
        for resource in _az_client.get_resources_in_group(resource_group):
            predictions_cache[resource_group][resource.id] = _get_prediction(resource_group, resource.id, now)
    print("Cache updated!")

def _get_prediction(resource_group: str, resource_id: str, latest_date: datetime.datetime = datetime.datetime.now()) -> Prediction:
    """
    Args:
        resource_group (str): The resource group identifier.
        resource_id (str): The resource identifier.
        latest_date (datetime.datetime, optional): The latest date to consider for the prediction. Defaults to datetime.datetime.now().

    Returns:
        Prediction: A prediction object for the given resource group and resource ID.
    """
    past_emissions = _az_client.get_emissions_for_resource(
        resource_group,
        resource_id,
        latest_date=latest_date,
        interval="PT1H"
    )

    three_days_time = datetime.datetime.now()+datetime.timedelta(days=3)
    try:
        return get_future_emissions(past_emissions, three_days_time)
    except ValueError:
        return {}

def get_resource_prediction(resource_group: str, *resource_ids: list[str]):
    """
    Args:
        resource_group (str): The resource group identifier.
        *resource_ids (list[str]): A list of resource identifiers.

    Returns:
        list[dict]: A sorted list of emissions predictions for the given resource group and resource IDs.
    """
    if len(resource_ids) == 0:
        resources_ids_in_group = map(lambda resource: resource.id, _az_client.get_resources_in_group(resource_group))
        return get_resource_prediction(resource_group, *list(resources_ids_in_group))
    
    emissions_sum = {}
    for resource_id in resource_ids:
        try:
            emissions = predictions_cache[resource_group][resource_id]
        except KeyError:
            emissions = predictions_cache[resource_group]["/"+resource_id]

        for data_point in emissions:
            date, value = data_point["date"], data_point["value"]
            if date not in emissions_sum:
                emissions_sum[date] = 0
            emissions_sum[date] += value
    
    return sorted(
        [{"date": date, "value": value} for date, value in emissions_sum.items()],
        key = lambda data_point: data_point["date"]
    )

def get_location_prediction(location: str, resource_group: str=None):
    """
    Args:
        location (str): The location identifier.
        resource_group (str, optional): The resource group identifier. Defaults to None.

    Returns:
        list[dict]: A sorted list of emissions predictions for the given location and resource group.
    """
    resources_in_groups: dict[str: GenericResourceExpanded] = _az_client.get_resources_at_location(location, resource_group)
    emissions_sum = {}

    for resource_group, resources in resources_in_groups.items():
        for resource in resources:
            try:
                emissions = predictions_cache[resource_group][resource.id]
            except KeyError:
                emissions = predictions_cache[resource_group]["/"+resource.id]

            for data_point in emissions:
                date, value = data_point["date"], data_point["value"]
                if date not in emissions_sum:
                    emissions_sum[date] = 0
                emissions_sum[date] += value
        
        return sorted(
            [{"date": date, "value": value} for date, value in emissions_sum.items()],
            key = lambda data_point: data_point["date"]
        )
            