from enum import Enum


class TimeInForce(str, Enum):
    GTC = "GTC"
    IOC = "IOC"
