from enum import Enum


class AdviceType(Enum):
    """
    An enumeration class representing different types of advice.
    
    Attributes:
        ENERGY_TYPE (int): Represents advice related to energy type.
        LOCATION (int): Represents advice related to location.
        RESOURCE_CONFIGURATION (int): Represents advice related to resource configuration.
        COOLING_TYPE (int): Represents advice related to cooling type.
    """
    ENERGY_TYPE = 1
    LOCATION = 2
    RESOURCE_CONFIGURATION = 3
    COOLING_TYPE = 4