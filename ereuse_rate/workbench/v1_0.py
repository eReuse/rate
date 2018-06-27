import math
from itertools import groupby
from operator import attrgetter
from typing import Iterable, List

from ereuse_devicehub.resources.device.models import Computer, DataStorage, RamModule, Processor
from ereuse_devicehub.resources.event.models import WorkbenchRate, BenchmarkDataStorage

from ereuse_rate.rate import BaseRate
from ereuse_rate.rate import DataStorageRate as _DataStorageRate
from ereuse_rate.rate import RamRate as _RamRate
from ereuse_rate.rate import ProcessorRate as _ProcessorRate


class Rate(BaseRate):
    def __init__(self) -> None:
        super().__init__()
        self.RATES = {
            DataStorage.t: DataStorageRate(),
            RamModule.t: RamRate(),
            Processor.t: ProcessorRate()
        }

    def compute(self, pc: Computer, rate: WorkbenchRate):
        """Compute rate"""
        assert isinstance(rate, WorkbenchRate)

        clause = attrgetter('type')
        for type, components in groupby(sorted(pc.components, key=clause), key=clause):
            self.RATES[type].compute(components, rate)

        # todo make something with all scores
        # todo return scores

    def filtering_and_cleaning_input(self, device: Computer):
        pass

    def component_characteristic_normalisation(self, device: Computer):
        super().component_characteristic_normalisation(device)

    def component_characteristic_rate(self, device: Computer):
        super().component_characteristic_rate(device)

    def component_fusion(self, device: Computer):
        super().component_fusion(device)

    def device_fusion(self, device: Computer):
        super().device_fusion(device)


class DataStorageRate(_DataStorageRate):
    """
    Calculate the rate of all DataStorage devices
    """
    WRITING_SPEED_FACTOR = 10000
    READING_SPEED_FACTOR = 3000

    SIZE_NORM = 4, 265000
    READ_SPEED_NORM = 2.7, 109.5
    WRITE_SPEED_NORM = 2, 27.35

    CEXP = 0
    """growing exponential from this value"""
    CLIN = 242
    """growing lineal starting on this value"""
    CLOG = 0.5
    """growing logaritmic starting on this value"""

    def filtering_and_cleaning_input(self, device: Computer):
        """
        Check if input device_type is desktop or laptop.
        Get and check all the data of components are valid to prepare it
        for post calculate device score.
        """
        pass

    def compute(self, storages: Iterable[DataStorage], rate: WorkbenchRate):
        """ """
        size = 0
        read_speed = 0
        write_speed = 0
        # STEP: Filtering, data cleaning and merging of component parts
        for storage in storages:
            benchmark = next(e for e in storage.events if isinstance(e, BenchmarkDataStorage))
            _size = storage.size or 0
            size += _size
            read_speed += benchmark.read_speed * _size
            write_speed += benchmark.write_speed * _size
        # Check almost one storage have size
        if size:
            read_speed /= size
            write_speed /= size
            # STEP: Normalize values
            size_norm = self.norm(size, *self.SIZE_NORM)
            read_speed_norm = self.norm(read_speed, *self.READ_SPEED_NORM)
            write_speed_norm = self.norm(write_speed, *self.WRITE_SPEED_NORM)
            # STEP: compute rate/score
            if size_norm >= self.CLOG:
                size_rate = self.rate_log(size_norm)
            elif self.CLIN <= size_norm < self.CLOG:
                size_rate = self.rate_lin(size_norm)
            elif self.CEXP <= size_norm < self.CLIN:
                size_rate = self.rate_exp(size_norm)


    def components_parts_fusion(self, device: object) -> object:
        return super().components_parts_fusion(device)

    def norm(self, x, x_min, x_max):
        return (x - x_min) / (x_max - x_min)

    def rate_exp(self, x):
        return math.exp(x) / (2 - math.exp(x))

    def rate_log(self, x):
        return math.log10(2*x) + 3.57 # todo magic number!

    def rate_lin(self, x):
        return 7*x + 0.06 # todo magic number!

    def harmonic_mean(self, chars: Iterable[float], rates: Iterable[float]):
        return sum(chars) / sum(char/rate for char, rate in zip(chars, rates))

class RamRate(_RamRate):
    """
    Calculate a RamRate of all RamModule devices
    """

    def compute(self, ram_device: Iterable[RamModule], rate: WorkbenchRate):
        pass

    def components_parts_fusion(self, device: object) -> object:
        return super().components_parts_fusion(device)


class ProcessorRate(_ProcessorRate):
    """
    Calculate a ProcessorRate of all Processor devices
    """

    def compute(self, processor_device: Iterable[Processor], rate: WorkbenchRate):
        pass

    def components_parts_fusion(self, device: object) -> object:
        return super().components_parts_fusion(device)
