import datetime
from typing import Callable

from azure.mgmt.resource.resources.models import GenericResourceExpanded

from .metrics_util import resource_metric

class ResourceCache:

    def __init__(self, refresh_time: int, fetch_resources: Callable) -> None:
        self._refresh_time: int = refresh_time
        self._resource_groups: dict[str: ResourceGroupCache] = {}
        self._fetch_resources: Callable = fetch_resources

    def get_resource(self, resource_group: str, resource_id: str) -> GenericResourceExpanded:
        self._update_resource_group(resource_group)
        return self._resource_groups[resource_group].get_resource(resource_id)  

    def get_resource_group(self, resource_group: str) -> list[GenericResourceExpanded]:
        self._update_resource_group(resource_group)
        return self._resource_groups[resource_group].resources

    def _update_resource_group(self, resource_group: str):
        if resource_group not in self._resource_groups or self._resource_groups[resource_group].time_since_update > self._refresh_time:
            resources_response = self._fetch_resources(resource_group)
            self._resource_groups[resource_group] = ResourceGroupCache(
                list(filter(lambda resource: resource.type in resource_metric, resources_response))
            )

class ResourceGroupCache:

    def __init__(self, resources: list[GenericResourceExpanded]):
        self._resources: dict[str, GenericResourceExpanded] = {
            resource.id: resource for resource in resources
        }
        self._timestamp = datetime.datetime.now()

    @property
    def time_since_update(self) -> float:
        return (datetime.datetime.now() - self._timestamp).total_seconds()
    
    @property
    def resources(self) -> list[GenericResourceExpanded]:
        return list(self._resources.values())
    
    def get_resource(self, resource_id: str) -> GenericResourceExpanded:
        if resource_id not in self._resources:
            raise KeyError(f"No such resource with id {resource_id}")
        
        return self._resources[resource_id]

def resource_to_dict(resource: GenericResourceExpanded):
    return {
        "id": resource.id,
        "name": resource.name,
        "type": resource.type,
        "location": resource.location,
        "extended_location": resource.extended_location,
        "tags": resource.tags,
        "kind": resource.kind,
        "managed_by": resource.managed_by,
        "sku": {
            "name": resource.sku.name,
            "tier": resource.sku.tier,
            "size": resource.sku.size,
            "family": resource.sku.family,
            "model": resource.sku.model,
            "capacity": resource.sku.capacity
        } if resource.sku else None,
        "identity": {
            "principal_id": resource.identity.principal_id,
            "tenant_id": resource.identity.tenant_id,
        } if resource.identity else None,
        "created_time": resource.created_time.strftime("%Y-%m-%d %H:%M:%S") if resource.created_time else None,
        "changed_time": resource.changed_time.strftime("%Y-%m-%d %H:%M:%S") if resource.changed_time else None,
    }