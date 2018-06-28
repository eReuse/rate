import pytest
from ereuse_devicehub.resources.device.models import Computer, HardDrive, RamModule, Processor
from ereuse_devicehub.resources.enums import FunctionalityRange, AppearanceRange
from ereuse_devicehub.resources.event.models import BenchmarkDataStorage, WorkbenchRate

from ereuse_rate.workbench.v1_0 import DataStorageRate, RamRate, ProcessorRate

""" LIST DUMMY COMPUTERS COMPONENTS CHARACTERISTICS

    pc_1193 = Computer()
    # add components characteristics of pc with id = 1193
    hdd_1969 = HardDrive(size=476940)
    hdd_1969.events_one.add(BenchmarkDataStorage(read_speed=126, write_speed=29.8))
    ram1 = RamModule(size=4096, speed=1600)
    ram2 = RamModule(size=2048, speed=1067)
    cpu = Processor(cores=2, speed=3.4)
    pc_1193.componets.add(hdd_1969, ram1, ram2, cpu)
    # add functionality and appearance range
    rate_pc_1193 = WorkbenchRate(appearance_range=AppearanceRange.A, functionality_range=FunctionalityRange.A)
    # add component rate
    HDD_rate = 4.02
    RAM_rate = 3.79
    Processor_rate = 3.95

    pc_1201 = Computer()
    hdd_3054 = HardDrive(size=476940)
    hdd_3054.events_one.add(BenchmarkDataStorage(read_speed=158, write_speed=34.7))
    ram1 = RamModule(size=2048, speed=1333)
    cpu = Processor(cores=2, speed=3.3)
    pc_1201.componets.add(hdd_3054, ram1, cpu)
    # add functionality and appearance range
    rate_pc_1201 = WorkbenchRate(appearance_range=AppearanceRange.B, functionality_range=FunctionalityRange.A)
    # add component rate
    HDD_rate = 4.07
    RAM_rate = 2.02
    Processor_rate = 3.93

    pc_79 = Computer()
    hdd_81 = HardDrive(size=76319)
    hdd_81.events_one.add(BenchmarkDataStorage(read_speed=72.2, write_speed=24.3))
    ram1 = RamModule(size=512, speed=667)
    ram2 = RamModule(size=512, speed=800)
    ram3 = RamModule(size=512, speed=667)
    ram4 = RamModule(size=512, speed=533)
    cpu = Processor(cores=1, speed=1.6)
    pc_79.componets.add(hdd_81, ram1, ram2, ram3, ram4, cpu)
    # add functionality and appearance range
    rate_pc_79 = WorkbenchRate(appearance_range=AppearanceRange.C, functionality_range=FunctionalityRange.A)
    # add component rate
    HDD_rate = 2.61
    RAM_rate = 1.99
    Processor_rate = 1

    pc_798 = Computer()
    hdd_1556 = HardDrive(size=152587)
    hdd_1556.events_one.add(BenchmarkDataStorage(read_speed=78.1, write_speed=24.4))
    ram0 = RamModule(size=0, speed=None)
    cpu = Processor(cores=2, speed=2.5)
    pc_798.componets.add(hdd_1556, ram0, cpu)
    # add functionality and appearance range
    rate_pc_798 = WorkbenchRate(appearance_range=AppearanceRange.B, functionality_range=FunctionalityRange.A)
    # add component rate
    HDD_rate = 3.7
    RAM_rate = 1
    Processor_rate = 4.09
"""

# DATA STORAGE DEVICE TEST

def test_data_storage_rate():
    """
    Test to check if compute data storage rate have same value than previous score version
    """
    hdd_1969 = HardDrive(size=476940)
    hdd_1969.events_one.add(BenchmarkDataStorage(read_speed=126, write_speed=29.8))

    # calculate DataStorage Rate, todo new fixture??
    data_storage_rate = DataStorageRate().compute([hdd_1969], WorkbenchRate())
    # expected score from previous rate version
    hdd_rate_old = 4.02
    # Limiting rate value to two decimal points
    hdd_rate_new = float("{0:.2f}".format(data_storage_rate))
    assert hdd_rate_new == hdd_rate_old, 'DataStorageRate returns incorrect value(rate)'

    hdd_3054 = HardDrive(size=476940)
    hdd_3054.events_one.add(BenchmarkDataStorage(read_speed=158, write_speed=34.7))
    # calculate DataStorage Rate
    data_storage_rate = DataStorageRate().compute([hdd_3054], WorkbenchRate())
    # expected score from previous rate version
    hdd_rate_old = 4.07
    # Limiting rate value to two decimal points
    hdd_rate_new = float("{0:.2f}".format(data_storage_rate))
    assert hdd_rate_new == hdd_rate_old, 'DataStorageRate returns incorrect value(rate)'

    hdd_81 = HardDrive(size=76319)
    hdd_81.events_one.add(BenchmarkDataStorage(read_speed=72.2, write_speed=24.3))
    data_storage_rate = DataStorageRate().compute([hdd_81], WorkbenchRate())
    # expected score from previous rate version
    hdd_rate_old = 2.61
    # Limiting rate value to two decimal points
    hdd_rate_new = float("{0:.2f}".format(data_storage_rate))
    assert hdd_rate_new == hdd_rate_old, 'DataStorageRate returns incorrect value(rate)'

    hdd_1556 = HardDrive(size=152587)
    hdd_1556.events_one.add(BenchmarkDataStorage(read_speed=78.1, write_speed=24.4))
    data_storage_rate = DataStorageRate().compute([hdd_81], WorkbenchRate())
    # expected score from previous rate version
    hdd_rate_old = 2.61
    # Limiting rate value to two decimal points
    hdd_rate_new = float("{0:.2f}".format(data_storage_rate))
    assert hdd_rate_new == hdd_rate_old, 'DataStorageRate returns incorrect value(rate)'


@pytest.mark.xfail(reason='Make test')
def test_data_storage_size_is_null():
    """
    Test where doing input DataStorage.size = NULL
    """


@pytest.mark.xfail(reason='Make test')
def test_data_storage_read_speed_is_0():
    """
    Test where BenchmarkDataStorage.read_speed = 0
    """


@pytest.mark.xfail(reason='Make test')
def test_data_storage_write_speed_is_0():
    """
    Test where BenchmarkDataStorage.write_speed = 0
    """

@pytest.mark.xfail(reason='Make test')
def test_no_data_storage():
    """
    Test with 0 data storage devices
    """

# RAM MODULE DEVICE TEST


def test_ram_rate():
    """
    Test to check if compute ram rate have same value than previous score version
    """
    # expected score from previous rate version
    ram_rate_old = 3.79

    ram1 = RamModule(size=4096, speed=1600)
    ram2 = RamModule(size=2048, speed=1067)

    # calculate Ram Rate, todo new fixture??
    ram_rate = RamRate().compute([ram1, ram2], WorkbenchRate())
    # Limiting rate value to two decimal points
    ram_rate_new = float("{0:.2f}".format(ram_rate))

    assert ram_rate_new == ram_rate_old, 'RamRate returns incorrect value(rate)'


@pytest.mark.xfail(reason='Make test')
def test_ram_size_is_0 ():
    """
    Test where doing input RamModule.size = 0
    """

@pytest.mark.xfail(reason='Make test')
def test_ram_speed_is_null():
    """
    Test where RamModule.speed is NULL
    """

@pytest.mark.xfail(reason='Make test')
def test_no_ram_modules():
    """
    Test where len(Collection[RamModule]) == 0
    """

# PROCESSOR DEVICE TEST

def test_processor_rate():
    """
    Test to check if compute processor rate have same value than previous score version
    """
    # expected score from previous rate version
    processor_rate_old = 3.95

    cpu = Processor(cores=2, speed=3.4)

    # calculate Processor Rate, todo new fixture??
    processor_rate = ProcessorRate().compute(cpu, WorkbenchRate())
    # Limiting rate value to two decimal points
    processor_rate_new = float("{0:.2f}".format(processor_rate))

    assert processor_rate_new == processor_rate_old, 'ProcessorRate returns incorrect value(rate)'


@pytest.mark.xfail(reason='Make test')
def test_processor_with_null_cores ():
    """
    Test with processor device have null number of cores
    """

@pytest.mark.xfail(reason='Make test')
def test_processor_with_null_speed():
    """
    Test with processor device have null speed value
    :return:
    """

@pytest.mark.xfail(reason='Make test')
def test_no_processor():
    """
    Test with any processor device
    :return:
    """