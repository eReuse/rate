import pytest
from ereuse_devicehub.resources.device.models import HardDrive, Processor, RamModule
from ereuse_devicehub.resources.event.models import BenchmarkDataStorage, BenchmarkProcessor, \
    WorkbenchRate

from ereuse_rate.workbench.v1_0 import DataStorageRate, ProcessorRate, RamRate

"""
Tests of compute rating for every component in a Device
Rates test done:
        -DataStorage
        -RamModule
        -Processor

Excluded cases in tests

- No Processor
-

"""


# DATA STORAGE DEVICE TEST


def test_data_storage_rate():
    """
    Test to check if compute data storage rate have same value than previous score version;
    id = pc_1193, pc_1201, pc_79, pc_798
    """

    hdd_1969 = HardDrive(size=476940)
    hdd_1969.events_one.add(BenchmarkDataStorage(read_speed=126, write_speed=29.8))

    data_storage_rate = DataStorageRate().compute([hdd_1969], WorkbenchRate())

    assert round(data_storage_rate, 2) == 4.02, 'DataStorageRate returns incorrect value(rate)'

    hdd_3054 = HardDrive(size=476940)
    hdd_3054.events_one.add(BenchmarkDataStorage(read_speed=158, write_speed=34.7))

    # calculate DataStorage Rate
    data_storage_rate = DataStorageRate().compute([hdd_3054], WorkbenchRate())

    assert round(data_storage_rate, 2) == 4.07, 'DataStorageRate returns incorrect value(rate)'

    hdd_81 = HardDrive(size=76319)
    hdd_81.events_one.add(BenchmarkDataStorage(read_speed=72.2, write_speed=24.3))

    data_storage_rate = DataStorageRate().compute([hdd_81], WorkbenchRate())

    assert round(data_storage_rate, 2) == 2.61, 'DataStorageRate returns incorrect value(rate)'

    hdd_1556 = HardDrive(size=152587)
    hdd_1556.events_one.add(BenchmarkDataStorage(read_speed=78.1, write_speed=24.4))

    data_storage_rate = DataStorageRate().compute([hdd_1556], WorkbenchRate())

    assert round(data_storage_rate, 2) == 3.70, 'DataStorageRate returns incorrect value(rate)'


def test_data_storage_size_is_null():
    """
    Test where input DataStorage.size = NULL, BenchmarkDataStorage.read_speed = 0,
    BenchmarkDataStorage.write_speed = 0 is like no DataStorage has been detected;
    id = pc_2992
    """

    hdd_null = HardDrive(size=None)
    hdd_null.events_one.add(BenchmarkDataStorage(read_speed=0, write_speed=0))

    data_storage_rate = DataStorageRate().compute([hdd_null], WorkbenchRate())
    assert data_storage_rate is None


def test_no_data_storage():
    """
    Test without data storage devices
    """
    hdd_null = HardDrive()
    hdd_null.events_one.add(BenchmarkDataStorage(read_speed=0, write_speed=0))
    data_storage_rate = DataStorageRate().compute([hdd_null], WorkbenchRate())
    assert data_storage_rate is None


# RAM MODULE DEVICE TEST


def test_ram_rate():
    """
    Test to check if compute ram rate have same value than previous score version
    only with 1 RamModule; id = pc_1201
    """

    ram1 = RamModule(size=2048, speed=1333)

    ram_rate = RamRate().compute([ram1], WorkbenchRate())

    assert round(ram_rate, 2) == 2.02, 'RamRate returns incorrect value(rate)'


def test_ram_rate_2modules():
    """
    Test to check if compute ram rate have same value than previous score version
    with 2 RamModule; id = pc_1193
    """

    ram1 = RamModule(size=4096, speed=1600)
    ram2 = RamModule(size=2048, speed=1067)

    ram_rate = RamRate().compute([ram1, ram2], WorkbenchRate())

    assert round(ram_rate, 2) == 3.79, 'RamRate returns incorrect value(rate)'


def test_ram_rate_4modules():
    """
    Test to check if compute ram rate have same value than previous score version
    with 2 RamModule; id = pc_79
    """

    ram1 = RamModule(size=512, speed=667)
    ram2 = RamModule(size=512, speed=800)
    ram3 = RamModule(size=512, speed=667)
    ram4 = RamModule(size=512, speed=533)

    ram_rate = RamRate().compute([ram1, ram2, ram3, ram4], WorkbenchRate())

    assert round(ram_rate, 2) == 1.99, 'RamRate returns incorrect value(rate)'


def test_ram_module_size_is_0():
    """
    Test where input data RamModule.size = 0; is like no RamModule has been detected; id =  pc_798
    """

    ram0 = RamModule(size=0, speed=888)

    ram_rate = RamRate().compute([ram0], WorkbenchRate())
    assert ram_rate is None


def test_ram_speed_is_null():
    """
    Test where RamModule.speed is NULL (not detected) but has size.
    Pc ID = 795(1542), 745(1535), 804(1549)
    """

    ram0 = RamModule(size=2048, speed=None)

    ram_rate = RamRate().compute([ram0], WorkbenchRate())

    assert round(ram_rate, 2) == 1.85, 'RamRate returns incorrect value(rate)'

    ram0 = RamModule(size=1024, speed=None)

    ram_rate = RamRate().compute([ram0], WorkbenchRate())

    assert round(ram_rate, 2) == 1.25, 'RamRate returns incorrect value(rate)'


def test_no_ram_module():
    """
    Test without RamModule
    """
    ram0 = RamModule()

    ram_rate = RamRate().compute([ram0], WorkbenchRate())
    assert ram_rate is None


# PROCESSOR DEVICE TEST

def test_processor_rate():
    """
    Test to check if compute processor rate have same value than previous score version
    only with 1 core; id = 79
    """

    cpu = Processor(cores=1, speed=1.6)
    # add score processor benchmark
    cpu.events_one.add(BenchmarkProcessor(rate=3192.34))

    processor_rate = ProcessorRate().compute(cpu, WorkbenchRate())

    assert processor_rate == 1, 'ProcessorRate returns incorrect value(rate)'


def test_processor_rate_2cores():
    """
    Test to check if compute processor rate have same value than previous score version
    with 2 cores; id = pc_1193, pc_1201
    """

    cpu = Processor(cores=2, speed=3.4)
    # add score processor benchmark
    cpu.events_one.add(BenchmarkProcessor(rate=27136.44))

    processor_rate = ProcessorRate().compute(cpu, WorkbenchRate())

    assert round(processor_rate, 2) == 3.95, 'ProcessorRate returns incorrect value(rate)'

    cpu = Processor(cores=2, speed=3.3)
    cpu.events_one.add(BenchmarkProcessor(rate=26339.48))

    processor_rate = ProcessorRate().compute(cpu, WorkbenchRate())

    assert round(processor_rate, 2) == 3.93, 'ProcessorRate returns incorrect value(rate)'


@pytest.mark.xfail(reason='Debug test')
def test_processor_with_null_cores():
    """
    Test with processor device have null number of cores
    """
    cpu = Processor(cores=None, speed=3.3)
    cpu.events_one.add(BenchmarkProcessor(rate=0))

    processor_rate = ProcessorRate().compute(cpu, WorkbenchRate())

    assert processor_rate == 1, 'ProcessorRate returns incorrect value(rate)'


@pytest.mark.xfail(reason='Debug test')
def test_processor_with_null_speed():
    """
    Test with processor device have null speed value
    """
    cpu = Processor(cores=1, speed=None)
    cpu.events_one.add(BenchmarkProcessor(rate=0))

    processor_rate = ProcessorRate().compute(cpu, WorkbenchRate())

    assert processor_rate == 1.06, 'ProcessorRate returns incorrect value(rate)'
