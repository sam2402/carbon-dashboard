import datetime
import os

from .metrics_util import resource_metric
from .emissions import get_carbon_coefficient
from .resource import ResourceCache

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import GenericResourceExpanded
from azure.mgmt.monitor import MonitorManagementClient

ONE_HOUR = 60*60

class AzureClient:
    def __init__(self):

        credential = DefaultAzureCredential()
        subscription_id = os.environ["SUBSCRIPTION_ID"]

        self.resource_client = ResourceManagementClient(credential, subscription_id)
        self.monitor_client = MonitorManagementClient(credential, subscription_id)

        self.resource_cache = ResourceCache(ONE_HOUR, self.resource_client.resources.list_by_resource_group)
    
    def _get_resource(self, resource_group: str, resource_id: str) -> GenericResourceExpanded:
        return self.resource_cache.get_resource(resource_group, resource_id)

    def get_resources_in_group(self, resource_group: str) -> list[GenericResourceExpanded]:
        return self.resource_cache.get_resource_group(resource_group)

    def get_emissions_for_resource_group(self,
                                resource_group: str,
                                earliest_date: datetime.datetime = None,
                                interval: str = None,
                                use_emissions_equivalent: bool = False
                                ) -> list[dict[str, float]]:
        if earliest_date is None:
            earliest_date = datetime.datetime.now().date()-datetime.timedelta(days=365)
        if interval is None:
            interval = "P1D"

        emissions_sum = {}
        for resource in self.get_resources_in_group(resource_group):
            emissions = self.get_emissions_for_resource(resource_group, resource.id, earliest_date, interval, use_emissions_equivalent)
            for data_point in emissions:
                date, value = data_point["date"], data_point["value"]
                if date not in emissions_sum:
                    emissions_sum[date] = 0
                emissions_sum[date] += value
        
        return sorted(
            [{"date": date, "value": value} for date, value in emissions_sum.items()],
            key = lambda data_point: data_point["date"]
        )

    def get_emissions_for_resource(self,
                                   resource_group: str,
                                   resource_id: str,
                                   earliest_date: datetime.datetime = None,
                                   interval: str = None,
                                   use_emissions_equivalent: bool = False
                                   ) -> list[dict[datetime.datetime, float]]:
        
        if earliest_date is None:
            earliest_date = datetime.datetime.now().date()-datetime.timedelta(days=700)
        if interval is None:
            interval = "P1D"

        resource = self._get_resource(resource_group, resource_id)

        try:
            metric = resource_metric[resource.type]
        except KeyError:
            raise Exception(f"Resource type: {resource.type} not supported")

        today = datetime.datetime.now().date()

        metrics_data = self.monitor_client.metrics.list(
            resource_id,
            timespan=f"{earliest_date}/{today}",
            interval=interval,
            metricnames=metric["name"],
            aggregation=metric["aggregation"]
        )

        data_points = []
        for item in metrics_data.value:
            for ts_element in item.timeseries:
                for data in ts_element.data:
                    computer_value_proxy = data.total if data.total is not None else 0
                    carbon_emissions = computer_value_proxy * get_carbon_coefficient(resource, data.time_stamp)
                    data_points.append({
                        "date": data.time_stamp,
                        "value": carbon_emissions
                    })
        
        return sorted(data_points, key = lambda data_point: data_point["date"])
