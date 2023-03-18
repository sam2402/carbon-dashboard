import datetime
import os

from .sources.objs import resource_metrics, location_zones
from .emissions import get_carbon_coefficient
from .resource import ResourceCache

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import GenericResourceExpanded, ResourceGroup
from azure.mgmt.monitor import MonitorManagementClient
from .electricity_mapper_api import ElectricityMapperClient

METRICS_RETENTION_PERIOD = 50

class AzureClient:

    _instance = None

    def __init__(self):

        credential = DefaultAzureCredential()
        subscription_id = os.environ["SUBSCRIPTION_ID"]

        self._resource_client = ResourceManagementClient(credential, subscription_id)
        self._monitor_client = MonitorManagementClient(credential, subscription_id)

        self._resource_cache = ResourceCache(
            datetime.timedelta(hours=1),
            self._resource_client.resources.list_by_resource_group,
            self._resource_client.resource_groups.list
        )
    
    # Implement AzureClient as a Singleton
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AzureClient, cls).__new__(cls)
        return cls._instance
    
    def _get_resource(self, resource_group: str, resource_id: str) -> GenericResourceExpanded:
        return self._resource_cache.get_resource(resource_group, resource_id)
    
    def get_resource_groups(self) -> list[str]:
        return self._resource_cache.get_resource_groups()

    def get_resources_in_group(self, resource_group: str) -> list[GenericResourceExpanded]:
        return self._resource_cache.get_resource_group(resource_group)

    def get_emissions_for_resource_group(self,
                                resource_group: str,
                                earliest_date: datetime.datetime = None,
                                latest_date: datetime.datetime = None,
                                interval: str = None,
                                ) -> list[dict[str, float]]:
        if earliest_date is None:
            earliest_date = datetime.datetime.now()-datetime.timedelta(days=METRICS_RETENTION_PERIOD)
        if latest_date is None:
            latest_date = datetime.datetime.now()
        if interval is None:
            interval = "P1D"

        emissions_sum = {}
        for resource in self.get_resources_in_group(resource_group):
            emissions = self.get_emissions_for_resource(resource_group, resource.id, earliest_date, latest_date, interval)
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
                                   latest_date: datetime.datetime = None,
                                   interval: str = None,
                                   ) -> list[dict[datetime.datetime, float]]:
        
        if earliest_date is None:
            earliest_date = datetime.datetime.now()-datetime.timedelta(days=METRICS_RETENTION_PERIOD)
        if latest_date is None:
            latest_date = datetime.datetime.now()
        if interval is None:
            interval = "P1D"

        resource = self._get_resource(resource_group, resource_id)

        try:
            metric = resource_metrics[resource.type]
        except KeyError:
            raise Exception(f"Resource type: {resource.type} not supported")

        metrics_data = self._monitor_client.metrics.list(
            resource_id,
            timespan=f"{earliest_date.date()}/{latest_date.date()}",
            interval=interval,
            metricnames=metric["name"],
            aggregation=metric["aggregation"]
        )

        location = resource.location
        lon, lat = location_zones[location]["longitude"], location_zones[location]["latitude"]
        emissions_over_time = ElectricityMapperClient().get_emissions_over_time(lon, lat, earliest_date, latest_date)
        
        data_points = []
        for item in metrics_data.value:
            for ts_element in item.timeseries:
                for data in ts_element.data:
                    computer_value_proxy = data.total if data.total is not None else 0
                    carbon_per_kwh = emissions_over_time[data.time_stamp.replace(minute=0, second=0, microsecond=0, tzinfo=None)]
                    carbon_emissions = computer_value_proxy * get_carbon_coefficient(resource, carbon_per_kwh, interval)
                    data_points.append({ 
                        "date": data.time_stamp,
                        "value": round(carbon_emissions, 6)
                    })
        
        return sorted(data_points, key = lambda data_point: data_point["date"])
