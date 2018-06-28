import math
from typing import Iterable

from ereuse_devicehub.resources.device.models import DataStorage, Device, Processor, RamModule
from ereuse_devicehub.resources.event.models import WorkbenchRate


class BaseRate:

    """growing exponential from this value"""
    CEXP = 0
    """growing lineal starting on this value"""
    CLIN = 242
    """growing logarithmic starting on this value"""
    CLOG = 0.5

    def compute(self, device: Device, rate: WorkbenchRate):
        raise NotImplementedError()

    @staticmethod
    def norm(x, x_min, x_max):
        return (x - x_min) / (x_max - x_min)

    @staticmethod
    def rate_log(x):
        return math.log10(2*x) + 3.57  # todo magic number!

    @staticmethod
    def rate_lin(x):
        return 7*x + 0.06  # todo magic number!

    @staticmethod
    def rate_exp(x):
        return math.exp(x) / (2 - math.exp(x))

    @staticmethod
    def harmonic_mean(weights: Iterable[float], rates: Iterable[float]):
        return sum(weights) / sum(char / rate for char, rate in zip(weights, rates))


class DataStorageRate(BaseRate):
    def compute(self, devices: Iterable[DataStorage], rate: WorkbenchRate):
        raise NotImplementedError()


class RamRate(BaseRate):
    def compute(self, devices: Iterable[RamModule], rate: WorkbenchRate):
        raise NotImplementedError()


class ProcessorRate(BaseRate):
    def compute(self, devices: Iterable[Processor], rate: WorkbenchRate):
        raise NotImplementedError()
