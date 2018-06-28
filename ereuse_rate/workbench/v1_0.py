from collections import namedtuple
from enum import Enum
from itertools import groupby
from operator import attrgetter
from typing import Iterable

from ereuse_devicehub.resources.device.models import Computer, DataStorage, RamModule, Processor
from ereuse_devicehub.resources.event.models import WorkbenchRate, BenchmarkDataStorage

from ereuse_rate.rate import BaseRate
from ereuse_rate.rate import DataStorageRate as _DataStorageRate
from ereuse_rate.rate import RamRate as _RamRate
from ereuse_rate.rate import ProcessorRate as _ProcessorRate


class Rate(BaseRate):
    """
    Rate all components in Computer
    """

    # Components general weights, Processor has 50%, Storage has 20%
    # and Ram has 30% of weight over total score, used in harmonic mean
    COMPONENTS_WEIGHTS = 0.5, 0.2, 0.3

    class Range(Enum):
        @classmethod
        def from_devicehub(cls, r: Enum):
            return getattr(cls, r.name) if r else cls.NONE

    class Appearance(Range):
        Z = 0.5
        A = 0.3
        B = 0
        C = -0.2
        D = -0.5
        E = -1.0
        NONE = -0.3

    class Functionality(Range):
        A = 0.4
        B = -0.5
        C = -0.75
        D = -1
        NONE = -0.3

    def __init__(self) -> None:
        super().__init__()
        self.RATES = {
            Processor.t: ProcessorRate(),
            RamModule.t: RamRate(),
            DataStorage.t: DataStorageRate(),
        }

    def compute(self, device: Computer, rate: WorkbenchRate):
        """Compute rate
            :return: result is a rate (score) ranging from 0 to 4.7 that represents estimating value of use
                    of desktop and laptop computer components
        """
        assert device.type == 'Desktop' or 'Laptop' or 'Server'
        assert isinstance(rate, WorkbenchRate)

        clause = attrgetter('type')
        rates = namedtuple('Rates', [DataStorage.t, Processor.t, RamModule.t])
        for type, components in groupby(sorted(device.components, key=clause), key=clause):
            setattr(rates, type, self.RATES[type].compute(components, rate))

        rate_components = self.harmonic_mean(*self.COMPONENTS_WEIGHTS, *rates)
        rate.appearance = self.Appearance.from_devicehub(rate.appearance_range).value
        rate.functionality = self.Functionality.from_devicehub(rate.functionality_range).value

        rate.rating = max(rate_components + rate.functionality + rate.appearance, 0)


class ProcessorRate(_ProcessorRate):
    """
    Calculate a ProcessorRate of all Processor devices
    """
    # processor.xMin, processor.xMax
    PROCESSOR_NORM = 3196.17, 17503.81

    DEFAULT_CORES = 1
    DEFAULT_SPEED = 1.6
    # In case of i2, i3,.. result penalized.
    # Intel(R) Core(TM) i3 CPU 530 @ 2.93GHz, score = 23406.92 but results inan score of 17503.
    # TODO: Multiply i1, i2,... for a constant
    DEFAULT_SCORE = 4000

    def compute(self, processor_device: Processor, rate: WorkbenchRate):
        """ Compute processor rate
            Obs: cores and speed are possible NULL value
            :return: result is a rate (score) of Processor characteristic
        """
        cores = processor_device.cores or self.DEFAULT_CORES
        speed = processor_device.speed or self.DEFAULT_SPEED

        # STEP: Fusion components
        processor_rate = (self.DEFAULT_SCORE + speed * 2000 * cores) / 2  # todo magic number!

        # STEP: Normalize values
        processor_norm = self.norm(processor_rate, *self.PROCESSOR_NORM) or 0

        # STEP: Compute rate/score from every component
        # Calculate processor_rate
        if processor_norm >= self.CEXP:
            processor_rate = self.rate_exp(processor_norm)
        if self.CLIN <= processor_norm < self.CLOG:
            processor_rate = self.rate_lin(processor_norm)
        if processor_norm >= self.CLOG:
            processor_rate = self.rate_log(processor_norm)

        rate.processor = processor_rate
        return rate.processor


class RamRate(_RamRate):
    """
    Calculate a RamRate of all RamModule devices
    """
    # ram.size.xMin; ram.size.xMax
    SIZE_NORM = 256, 8192
    RAM_SPEED_NORM = 133, 1333
    # ram.size.weight; ram.speed.weight;
    RAM_WEIGHTS = 0.7, 0.3

    def compute(self, ram_devices, rate: WorkbenchRate):
        """
        Obs: RamModule.speed is possible NULL value & size != NULL or NOT??
        :return: result is a rate (score) of all RamModule components
        """
        size = 0
        speed = 0

        # STEP: Filtering, data cleaning and merging of component parts
        for ram in ram_devices:
            size += ram.size or 0
            speed += (ram.speed or 0) * size

        # STEP: Fusion components
        # Check almost have one ram module
        if ram_devices:
            speed /= len(ram_devices)

        # STEP: Normalize values
            size_norm = self.norm(size, *self.SIZE_NORM)
            ram_speed_norm = self.norm(speed, *self.RAM_SPEED_NORM)

        # STEP: Compute rate/score from every component
            # Calculate size_rate
            if self.CEXP <= size_norm < self.CLIN:
                size_rate = self.rate_exp(size_norm)
            if self.CLIN <= size_norm < self.CLOG:
                size_rate = self.rate_lin(size_norm)
            if size_norm >= self.CLOG:
                size_rate = self.rate_log(size_norm)
            # Calculate read_speed_rate
            if self.CEXP <= size_norm < self.CLIN:
                ram_speed_rate = self.rate_exp(ram_speed_norm)
            if self.CLIN <= ram_speed_norm < self.CLOG:
                ram_speed_rate = self.rate_lin(ram_speed_norm)
            if ram_speed_norm >= self.CLOG:
                ram_speed_rate = self.rate_log(ram_speed_norm)

        # STEP: Fusion Characteristics
            ram_rates = size_rate, ram_speed_rate
            rate.ram = self.harmonic_mean(self.RAM_WEIGHTS, ram_rates)
            return rate.ram
        else:
            return 0


class DataStorageRate(_DataStorageRate):
    """
    Calculate the rate of all DataStorage devices
    """
    # drive.size.xMin; drive.size.xMax
    SIZE_NORM = 4, 265000
    READ_SPEED_NORM = 2.7, 109.5
    WRITE_SPEED_NORM = 2, 27.35
    # drive.size.weight; drive.readingSpeed.weight; drive.writingSpeed.weight;
    DATA_STORAGE_WEIGHTS = 0.5, 0.25, 0.25

    def compute(self, data_storage_devices: Iterable[DataStorage], rate: WorkbenchRate):
        """
        Obs: size is possible NULL value & read_speed and write_speed != NULL
        :return: result is a rate (score) of all DataStorage devices
        """
        size = 0
        read_speed = 0
        write_speed = 0

        # STEP: Filtering, data cleaning and merging of component parts
        for storage in data_storage_devices:
            benchmark = next(e for e in storage.events if isinstance(e, BenchmarkDataStorage))
            # prevent NULL value
            _size = storage.size or 0
            size += _size
            read_speed += benchmark.read_speed * _size
            write_speed += benchmark.write_speed * _size

        # STEP: Fusion components
        # Check almost one storage have size, try catch exception 0/0
        if size:
            read_speed /= size
            write_speed /= size

        # STEP: Normalize values
            size_norm = self.norm(size, *self.SIZE_NORM)
            read_speed_norm = self.norm(read_speed, *self.READ_SPEED_NORM)
            write_speed_norm = self.norm(write_speed, *self.WRITE_SPEED_NORM)

        # STEP: Compute rate/score from every component
            # Calculate size_rate
            if size_norm >= self.CLOG:
                size_rate = self.rate_log(size_norm)
            elif self.CLIN <= size_norm < self.CLOG:
                size_rate = self.rate_lin(size_norm)
            elif self.CEXP <= size_norm < self.CLIN:
                size_rate = self.rate_exp(size_norm)
            # Calculate read_speed_rate
            if read_speed_norm >= self.CLOG:
                read_speed_rate = self.rate_log(read_speed_norm)
            elif self.CLIN <= read_speed_norm < self.CLOG:
                read_speed_rate = self.rate_lin(read_speed_norm)
            elif self.CEXP <= read_speed_norm < self.CLIN:
                read_speed_rate = self.rate_exp(read_speed_norm)
            # write_speed_rate
            if write_speed_norm >= self.CLOG:
                write_speed_rate = self.rate_log(write_speed_norm)
            elif self.CLIN <= write_speed_norm < self.CLOG:
                write_speed_rate = self.rate_lin(write_speed_norm)
            elif self.CEXP <= write_speed_norm < self.CLIN:
                write_speed_rate = self.rate_exp(write_speed_norm)

        # STEP: Fusion Characteristics
            data_storage_rates = size_rate, read_speed_rate, write_speed_rate
            rate.data_storage = self.harmonic_mean(self.DATA_STORAGE_WEIGHTS, data_storage_rates)
            return rate.data_storage
        else:
            return 0
