import pytest
from ereuse_devicehub.resources.device.models import HardDrive, RamModule, Processor
from ereuse_devicehub.resources.event.models import BenchmarkDataStorage, WorkbenchRate, \
    BenchmarkProcessor

from ereuse_rate.workbench.v1_0 import DataStorageRate, RamRate, ProcessorRate


# DATA STORAGE DEVICE TEST


def test_data_storage_rate():
    """
    Test to check if compute data storage rate have same value than previous score version
    """
    # expected score from previous rate version of pc_1193
    hdd_rate_old = 4.02
    hdd_1969 = HardDrive(size=476940)
    hdd_1969.events_one.add(BenchmarkDataStorage(read_speed=126, write_speed=29.8))

    # calculate DataStorage Rate, todo new fixture??
    data_storage_rate = DataStorageRate().compute([hdd_1969], WorkbenchRate())
    # Limiting rate value to two decimal points
    hdd_rate_new = float("{0:.2f}".format(data_storage_rate))

    assert hdd_rate_old == hdd_rate_new, 'DataStorageRate returns incorrect value(rate)'

    # expected score from previous rate version of pc_1201
    hdd_rate_old = 4.07
    hdd_3054 = HardDrive(size=476940)
    hdd_3054.events_one.add(BenchmarkDataStorage(read_speed=158, write_speed=34.7))

    # calculate DataStorage Rate
    data_storage_rate = DataStorageRate().compute([hdd_3054], WorkbenchRate())
    # Limiting rate value to two decimal points
    hdd_rate_new = float("{0:.2f}".format(data_storage_rate))

    assert hdd_rate_old == hdd_rate_new, 'DataStorageRate returns incorrect value(rate)'

    # expected score from previous rate version of pc_79
    hdd_rate_old = 2.61
    hdd_81 = HardDrive(size=76319)
    hdd_81.events_one.add(BenchmarkDataStorage(read_speed=72.2, write_speed=24.3))

    data_storage_rate = DataStorageRate().compute([hdd_81], WorkbenchRate())
    # Limiting rate value to two decimal points
    hdd_rate_new = float("{0:.2f}".format(data_storage_rate))

    assert hdd_rate_old == hdd_rate_new, 'DataStorageRate returns incorrect value(rate)'

    # expected score from previous rate version of pc_798
    hdd_rate_old = 3.7
    hdd_1556 = HardDrive(size=152587)
    hdd_1556.events_one.add(BenchmarkDataStorage(read_speed=78.1, write_speed=24.4))

    data_storage_rate = DataStorageRate().compute([hdd_1556], WorkbenchRate())
    # Limiting rate value to two decimal points
    hdd_rate_new = float("{0:.2f}".format(data_storage_rate))

    assert hdd_rate_old == hdd_rate_new, 'DataStorageRate returns incorrect value(rate)'


def test_data_storage_size_is_null():
    """
    Test where input DataStorage.size = NULL, BenchmarkDataStorage.read_speed = 0,
    BenchmarkDataStorage.write_speed = 0 is like no DataStorage has been detected
    """
    # expected score from previous rate version of pc_2992
    hdd_rate_old = 1
    hdd_null = HardDrive(size=None)
    hdd_null.events_one.add(BenchmarkDataStorage(read_speed=0, write_speed=0))

    data_storage_rate = DataStorageRate().compute([hdd_null], WorkbenchRate())
    # Limiting rate value to two decimal points
    hdd_rate_new = float("{0:.2f}".format(data_storage_rate))

    assert hdd_rate_old == hdd_rate_new, 'DataStorageRate returns incorrect value(rate)'


@pytest.mark.xfail(reason='Debug test')
def test_no_data_storage():
    """
    Test without data storage devices
    """
    hdd_rate_old = 1
    hdd_null = HardDrive()

    data_storage_rate = DataStorageRate().compute([hdd_null], WorkbenchRate())
    # Limiting rate value to two decimal points
    hdd_rate_new = float("{0:.2f}".format(data_storage_rate))

    assert hdd_rate_old == hdd_rate_new, 'DataStorageRate returns incorrect value(rate)'


# RAM MODULE DEVICE TEST


def test_ram_rate():
    """
    Test to check if compute ram rate have same value than previous score version
    only with 1 RamModule
    """

    # expected score from previous rate version of pc_1201
    ram_rate_old = 2.02

    ram1 = RamModule(size=2048, speed=1333)

    # calculate Ram Rate, todo new fixture??
    ram_rate = RamRate().compute([ram1], WorkbenchRate())
    # Limiting rate value to two decimal points
    ram_rate_new = float("{0:.2f}".format(ram_rate))

    assert ram_rate_old == ram_rate_new, 'RamRate returns incorrect value(rate)'


def test_ram_rate_2modules():
    """
    Test to check if compute ram rate have same value than previous score version
    with 2 RamModule
    """
    # expected score from previous rate version of pc_1193
    ram_rate_old = 3.79

    ram1 = RamModule(size=4096, speed=1600)
    ram2 = RamModule(size=2048, speed=1067)

    ram_rate = RamRate().compute([ram1, ram2], WorkbenchRate())
    # Limiting rate value to two decimal points
    ram_rate_new = float("{0:.2f}".format(ram_rate))

    assert ram_rate_old == ram_rate_new, 'RamRate returns incorrect value(rate)'


def test_ram_rate_4modules():
    """
    Test to check if compute ram rate have same value than previous score version
    with 2 RamModule
    """
    # expected score from previous rate version of pc_79
    ram_rate_old = 1.99

    ram1 = RamModule(size=512, speed=667)
    ram2 = RamModule(size=512, speed=800)
    ram3 = RamModule(size=512, speed=667)
    ram4 = RamModule(size=512, speed=533)

    ram_rate = RamRate().compute([ram1, ram2, ram3, ram4], WorkbenchRate())
    # Limiting rate value to two decimal points
    ram_rate_new = float("{0:.2f}".format(ram_rate))

    assert ram_rate_old == ram_rate_new, 'RamRate returns incorrect value(rate)'


def test_ram_module_size_is_0():
    """
    Test where input data RamModule.size = 0; is like no RamModule has been detected
    """
    # expected score from previous rate version of pc_798
    ram_rate_old = 1

    ram0 = RamModule(size=0, speed=888)

    ram_rate = RamRate().compute([ram0], WorkbenchRate())
    # Limiting rate value to two decimal points
    ram_rate_new = float("{0:.2f}".format(ram_rate))

    assert ram_rate_old == ram_rate_new, 'RamRate returns incorrect value(rate)'


def test_ram_speed_is_null():
    """
    Test where RamModule.speed is NULL (not detected) but has size
    """
    # expected score from previous rate version on pc_804
    # todo check previous score, find a pc with speed == NULL
    ram_rate_old = 1.85

    ram0 = RamModule(size=2048, speed=None)

    ram_rate = RamRate().compute([ram0], WorkbenchRate())
    # Limiting rate value to two decimal points
    ram_rate_new = float("{0:.2f}".format(ram_rate))

    assert ram_rate_old == ram_rate_new, 'RamRate returns incorrect value(rate)'


@pytest.mark.xfail(reason='Duplicate test')
def test_no_ram_module():
    """
    Test without RamModule
    """
    ram_rate_old = 1

    ram0 = RamModule()

    ram_rate = RamRate().compute([ram0], WorkbenchRate())
    # Limiting rate value to two decimal points
    ram_rate_new = float("{0:.2f}".format(ram_rate))

    assert ram_rate_old == ram_rate_new, 'RamRate returns incorrect value(rate)'

# PROCESSOR DEVICE TEST


def test_processor_rate():
    """
    Test to check if compute processor rate have same value than previous score version
    only with 1 core
    """

    # expected score from previous rate version of pc_79
    processor_rate_old = 1

    cpu = Processor(cores=1, speed=1.6)
    # add score processor benchmark
    cpu.events_one.add(BenchmarkProcessor(rate=3192.34))

    # calculate Processor Rate, todo new fixture??
    processor_rate = ProcessorRate().compute(cpu, WorkbenchRate())
    # Limiting rate value to two decimal points
    processor_rate_new = float("{0:.2f}".format(processor_rate))

    assert processor_rate_new == processor_rate_old, 'ProcessorRate returns incorrect value(rate)'


def test_processor_rate_2cores():
    """
    Test to check if compute processor rate have same value than previous score version
    with 2 cores
    """
    # expected score from previous rate version of pc_1193
    processor_rate_old = 3.95

    cpu = Processor(cores=2, speed=3.4)
    # add score processor benchmark
    cpu.events_one.add(BenchmarkProcessor(rate=27136.44))

    processor_rate = ProcessorRate().compute(cpu, WorkbenchRate())
    # Limiting rate value to two decimal points
    processor_rate_new = float("{0:.2f}".format(processor_rate))

    assert processor_rate_new == processor_rate_old, 'ProcessorRate returns incorrect value(rate)'

    # expected score from previous rate version of pc_1201
    processor_rate_old = 3.93

    cpu = Processor(cores=2, speed=3.3)
    cpu.events_one.add(BenchmarkProcessor(rate=26339.48))

    processor_rate = ProcessorRate().compute(cpu, WorkbenchRate())
    # Limiting rate value to two decimal points
    processor_rate_new = float("{0:.2f}".format(processor_rate))

    assert processor_rate_new == processor_rate_old, 'ProcessorRate returns incorrect value(rate)'


@pytest.mark.xfail(reason='Debug test')
def test_processor_with_null_cores():
    """
    Test with processor device have null number of cores
    """
    cpu = Processor(cores=None, speed=3.3)
    cpu.events_one.add(BenchmarkProcessor(rate=0))

    processor_rate = ProcessorRate().compute(cpu, WorkbenchRate())
    # Limiting rate value to two decimal points
    processor_rate_new = float("{0:.2f}".format(processor_rate))
    # todo processor_rate_old == 1??

    assert processor_rate_new == 1, 'ProcessorRate returns incorrect value(rate)'


@pytest.mark.xfail(reason='Debug test')
def test_processor_with_null_speed():
    """
    Test with processor device have null speed value
    """
    cpu = Processor(cores=1, speed=None)
    cpu.events_one.add(BenchmarkProcessor(rate=0))

    processor_rate = ProcessorRate().compute(cpu, WorkbenchRate())
    # Limiting rate value to two decimal points
    processor_rate_new = float("{0:.2f}".format(processor_rate))
    # todo processor_rate_old == 1.06 ??

    assert processor_rate_new == 1.06, 'ProcessorRate returns incorrect value(rate)'


@pytest.mark.xfail(reason='Debug test')
def test_no_processor():
    """
    Test with any processor device
    """
    cpu = Processor()

    processor_rate = ProcessorRate().compute(cpu, WorkbenchRate())
    # Limiting rate value to two decimal points
    processor_rate_new = float("{0:.2f}".format(processor_rate))
    # todo processor_rate_old == 1 ??

    assert processor_rate_new == 1, 'ProcessorRate returns incorrect value(rate)'
