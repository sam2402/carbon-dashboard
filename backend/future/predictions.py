import datetime

from ..carbon.azure_api import AzureClient
from .Model import get_future_emissions

Prediction = list[dict[str, str | float]]

predictions_cache: dict[str, dict[str, Prediction]] = {}
_az_client: AzureClient = AzureClient()

def update_cache():
    now = datetime.datetime.now()
    for resource_group in _az_client.get_resource_groups():
        predictions_cache[resource_group] = {}
        for resource in _az_client.get_resources_in_group(resource_group):
            predictions_cache[resource_group][resource.id] = _get_prediction(resource_group, resource.id, now)
    print(predictions_cache)
    print("Cache updated!")

def _get_prediction(resource_group: str, resource_id: str, latest_date: datetime.datetime = datetime.datetime.now()) -> Prediction:
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


