import json
import os

with open("./carbon/sources/resource_metrics.json") as rms_file:
    resource_metrics = json.load(rms_file)

with open("./carbon/sources/cpus.json") as cpus_file:
    cpus = json.load(cpus_file)

with open("./carbon/sources/location_zones.json") as cpus_file:
    location_zones = json.load(cpus_file)