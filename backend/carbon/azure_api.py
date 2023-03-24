import datetime
import os

from .sources.objs import resource_metrics, location_zones
from .emissions import get_carbon_coefficient
from .resource import ResourceCache
from .electricity_mapper_api import ElectricityMapperClient


from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import GenericResourceExpanded
from azure.mgmt.monitor import MonitorManagementClient
from cachetools import cached, TTLCache

METRICS_RETENTION_PERIOD = 50

class AzureClient:
    """
    A Singleton class that used to interacting with the Azure API can fetch resource data and carbon emissions data.
    """


    _instance = None

    def __init__(self):
        """
        Initializes the AzureClient object with required credentials and clients.
        """

        credential = DefaultAzureCredential()
        subscription_id = os.environ["SUBSCRIPTION_ID"]

        self._resource_client = ResourceManagementClient(credential, subscription_id)
        self._monitor_client = MonitorManagementClient(credential, subscription_id)

        self._resource_cache = ResourceCache(
            datetime.timedelta(hours=2),
            self._resource_client.resources.list_by_resource_group,
            self._resource_client.resource_groups.list
        )
    
    # Implement AzureClient as a Singleton
    def __new__(cls):
        """
        Guarantees that only one instance of AzureClient is generated, according to the Singleton design principle        
        
        Returns:
            AzureClient: The unique instance of the AzureClient class.
        """
        if cls._instance is None:
            cls._instance = super(AzureClient, cls).__new__(cls)
        return cls._instance
    
    def get_resource(self, resource_group: str, resource_id: str) -> GenericResourceExpanded:
        """
        Retrieves a specific resource from the cache with its specific resource group and resource ID.

        Args:
            resource_group (str): The name of the specific resource group.
            resource_id (str): The unique ID of the specific resource.
        
        Returns:
            GenericResourceExpanded: The requested resource information from Azure.
        """
        return self._resource_cache.get_resource(resource_group, resource_id)
    
    def get_resource_groups(self) -> list[str]:
        """
        Retrieves a list of all available resource groups.

        Returns:
            list[str]: A list of resource group names.
        """
        return self._resource_cache.get_resource_groups()

    def get_resources_in_group(self, resource_group: str) -> list[GenericResourceExpanded]:
        """
        Retrieves all resources in a specific resource group.

        Args:
            resource_group (str): The name of the resource group.

        Returns:
            list[GenericResourceExpanded]: A list of resources information within the specific resource group.
        """
        return self._resource_cache.get_resource_group(resource_group)

    def get_resources_at_location(self, location: str, resource_group: str=None) -> dict[str: GenericResourceExpanded]:
        """
        Obtains resources from a certain place, with the option of filtering by a resource group.

        Args:
            location (str): The location to obtains resources from.
            resource_group (str, optional): The resource group to filter resources by.

        Returns:
            dict[str, GenericResourceExpanded]: A dictionary of resource groups and their resource information at the specified location.
        """
        resources = {}
        for resource_group_name in self.get_resource_groups():
            if resource_group is None or resource_group_name == resource_group:
                resources[resource_group_name] = []
                for resource in self.get_resources_in_group(resource_group_name):
                    if resource.location == location:
                        resources[resource_group_name].append(resource)
        return resources
                
    def get_emissions_for_resource_group(self,
                                resource_group: str,
                                earliest_date: datetime.datetime = None,
                                latest_date: datetime.datetime = None,
                                interval: str = None,
                                ) -> list[dict[str, float]]:
        """
        Retrieves carbon emissions data for a specific resource group within a specified date range and given time interval.

        Args:
            resource_group (str): The name of the resource group.
            earliest_date (datetime.datetime, optional): The start date for specified date range of carbon emissions data.
            latest_date (datetime.datetime, optional): The end date for specified date range of carbon emissions data.
            interval (str, optional): The time interval for the emissions data.

        Returns:
            list[dict[str, float]]: A list of dictionaries in format of date and emissions value.
        """
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

    @cached(cache = TTLCache(maxsize = 32, ttl = datetime.timedelta(hours=1), timer=datetime.datetime.now)) 
    def get_emissions_for_resource(self,
                                   resource_group: str,
                                   resource_id: str,
                                   earliest_date: datetime.datetime = None,
                                   latest_date: datetime.datetime = None,
                                   interval: str = None,
                                   ) -> list[dict[datetime.datetime, float]]:
        """
        Retrieves carbon emissions data for a specific resource within a specified date range and interval.

        Args:
            resource_group (str): The name of the given resource group.
            resource_id (str): The unique ID of the specific resource.
            earliest_date (datetime.datetime, optional): The start date for specified date range of carbon emissions data.
            latest_date (datetime.datetime, optional): The end date for specified date range of carbon emissions data.
            interval (str, optional): The time interval for the emissions data.

        Returns:
            list[dict[datetime.datetime, float]]: A list of dictionaries in format of date and emissions value.
        """
        
        if earliest_date is None:
            earliest_date = datetime.datetime.now()-datetime.timedelta(days=METRICS_RETENTION_PERIOD)
        if latest_date is None:
            latest_date = datetime.datetime.now()
        if interval is None:
            interval = "P1D"

        resource = self.get_resource(resource_group, resource_id)

        try:
            metric = resource_metrics[resource.type]
        except KeyError:
            raise Exception(f"Resource type: {resource.type} not supported")

        metrics_data = self._monitor_client.metrics.list(
            resource_id,
            timespan=f"{earliest_date}/{latest_date}",
            interval=interval,
            metricnames=metric["name"],
            aggregation=metric["aggregation"]
        )

        location = resource.location
        lon, lat = location_zones[location]["longitude"], location_zones[location]["latitude"]
        emissions_over_time = ElectricityMapperClient().get_emissions_over_time(
            lon,
            lat,
            earliest_date-datetime.timedelta(days=1),
            max(latest_date+datetime.timedelta(days=1), datetime.datetime.now())
        )
        print(emissions_over_time, sep="\n") 
        data_points = []
        for item in metrics_data.value:
            for ts_element in item.timeseries:
                for data in ts_element.data:
                    computer_value_proxy = data.total if data.total is not None else 0
                    carbon_per_kwh = emissions_over_time[data.time_stamp.replace(minute=0, second=0, microsecond=0, tzinfo=None)]
                    carbon_emissions = computer_value_proxy * get_carbon_coefficient(resource, carbon_per_kwh, interval)
                    data_points.append({ 
                        "date": data.time_stamp,
                        "value": round(carbon_emissions, 1)
                    })
        
        return sorted(data_points, key = lambda data_point: data_point["date"])
