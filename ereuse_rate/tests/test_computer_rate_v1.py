from ereuse_devicehub.resources.device.models import Desktop, HardDrive, Processor, RamModule
from ereuse_devicehub.resources.enums import AppearanceRange, FunctionalityRange
from ereuse_devicehub.resources.event.models import BenchmarkDataStorage, BenchmarkProcessor, \
    WorkbenchRate

from ereuse_rate.workbench.v1_0 import Rate

""" LIST DUMMIES COMPUTERS COMPONENTS CHARACTERISTICS

    pc_1193 = Computer()
    price = 92.2
    # add components characteristics of pc with id = 1193
    hdd_1969 = HardDrive(size=476940)
    hdd_1969.events_one.add(BenchmarkDataStorage(read_speed=126, write_speed=29.8))
    ram1 = RamModule(size=4096, speed=1600)
    ram2 = RamModule(size=2048, speed=1067)
    cpu = Processor(cores=2, speed=3.4)
    cpu.events_one.add(BenchmarkProcessor(rate=27136.44))
    pc_1193.components.add(hdd_1969, ram1, ram2, cpu)
    # add functionality and appearance range
    rate_pc_1193 = WorkbenchRate(appearance_range=AppearanceRange.A, functionality_range=FunctionalityRange.A)
    # add component rate
    HDD_rate = 4.02
    RAM_rate = 3.79
    Processor_rate = 3.95
    Rating = 4.61

    pc_1201 = Computer()
    price = 69.6
    hdd_3054 = HardDrive(size=476940)
    hdd_3054.events_one.add(BenchmarkDataStorage(read_speed=158, write_speed=34.7))
    ram1 = RamModule(size=2048, speed=1333)
    cpu = Processor(cores=2, speed=3.3)
    cpu.events_one.add(BenchmarkProcessor(rate=26339.48))
    pc_1201.components.add(hdd_3054, ram1, cpu)
    # add functionality and appearance range
    rate_pc_1201 = WorkbenchRate(appearance_range=AppearanceRange.B, functionality_range=FunctionalityRange.A)
    # add component rate
    HDD_rate = 4.07
    RAM_rate = 2.02
    Processor_rate = 3.93
    Rating = 3.48

    pc_79 = Computer()
    price = VeryLow
    hdd_81 = HardDrive(size=76319)
    hdd_81.events_one.add(BenchmarkDataStorage(read_speed=72.2, write_speed=24.3))
    ram1 = RamModule(size=512, speed=667)
    ram2 = RamModule(size=512, speed=800)
    ram3 = RamModule(size=512, speed=667)
    ram4 = RamModule(size=512, speed=533)
    cpu = Processor(cores=1, speed=1.6)
    cpu.events_one.add(BenchmarkProcessor(rate=3192.34))
    pc_79.components.add(hdd_81, ram1, ram2, ram3, ram4, cpu)
    # add functionality and appearance range
    rate_pc_79 = WorkbenchRate(appearance_range=AppearanceRange.C, functionality_range=FunctionalityRange.A)
    # add component rate
    HDD_rate = 2.61
    RAM_rate = 1.99
    Processor_rate = 1
    Rating = 1.58

    pc_798 = Computer()
    price = 50
    hdd_1556 = HardDrive(size=152587)
    hdd_1556.events_one.add(BenchmarkDataStorage(read_speed=78.1, write_speed=24.4))
    ram0 = RamModule(size=0, speed=None)
    cpu = Processor(cores=2, speed=2.5)
    cpu.events_one.add(BenchmarkProcessor(rate=9974.3))
    pc_798.components.add(hdd_1556, ram0, cpu)
    # add functionality and appearance range
    rate_pc_798 = WorkbenchRate(appearance_range=AppearanceRange.B, functionality_range=FunctionalityRange.A)
    # add component rate
    HDD_rate = 3.7
    RAM_rate = 1
    Processor_rate = 4.09
    Rating = 2.5
"""


def test_computer_rate():
    """
    Test Rate v1
    """
    # Create a new Computer with components characteristics of pc with id = 1193
    pc_test = Desktop()
    data_storage = HardDrive(size=476940)
    data_storage.events_one.add(BenchmarkDataStorage(read_speed=126, write_speed=29.8))
    cpu = Processor(cores=2, speed=3.4)
    cpu.events_one.add(BenchmarkProcessor(rate=27136.44))
    pc_test.components |= {
        data_storage,
        RamModule(size=4096, speed=1600),
        RamModule(size=2048, speed=1067),
        cpu
    }
    # add functionality and appearance range
    rate_pc = WorkbenchRate(appearance_range=AppearanceRange.A,
                            functionality_range=FunctionalityRange.A)
    # Compute all components rates and general rating
    Rate().compute(pc_test, rate_pc)

    assert round(rate_pc.ram, 2) == 3.79

    assert round(rate_pc.data_storage, 2) == 4.02

    assert round(rate_pc.processor, 2) == 3.95

    assert round(rate_pc.rating, 2) == 4.61

    # Create a new Computer with components characteristics of pc with id = 1201
    pc_test = Desktop()
    data_storage = HardDrive(size=476940)
    data_storage.events_one.add(BenchmarkDataStorage(read_speed=158, write_speed=34.7))
    cpu = Processor(cores=2, speed=3.3)
    cpu.events_one.add(BenchmarkProcessor(rate=26339.48))
    pc_test.components |= {
        data_storage,
        RamModule(size=2048, speed=1333),
        cpu
    }
    # add functionality and appearance range
    rate_pc = WorkbenchRate(appearance_range=AppearanceRange.B,
                            functionality_range=FunctionalityRange.A)
    # Compute all components rates and general rating
    Rate().compute(pc_test, rate_pc)

    assert round(rate_pc.ram, 2) == 2.02

    assert round(rate_pc.data_storage, 2) == 4.07

    assert round(rate_pc.processor, 2) == 3.93

    assert round(rate_pc.rating, 2) == 3.48

    # Create a new Computer with components characteristics of pc with id = 79
    pc_test = Desktop()
    data_storage = HardDrive(size=76319)
    data_storage.events_one.add(BenchmarkDataStorage(read_speed=72.2, write_speed=24.3))
    cpu = Processor(cores=1, speed=1.6)
    cpu.events_one.add(BenchmarkProcessor(rate=3192.34))
    pc_test.components |= {
        data_storage,
        RamModule(size=512, speed=667),
        RamModule(size=512, speed=800),
        RamModule(size=512, speed=667),
        RamModule(size=512, speed=533),
        cpu
    }
    # add functionality and appearance range
    rate_pc = WorkbenchRate(appearance_range=AppearanceRange.C,
                            functionality_range=FunctionalityRange.A)
    # Compute all components rates and general rating
    Rate().compute(pc_test, rate_pc)

    assert round(rate_pc.ram, 2) == 1.99

    assert round(rate_pc.data_storage, 2) == 2.61

    assert round(rate_pc.processor, 2) == 1

    assert round(rate_pc.rating, 2) == 1.58

# Create a new Computer with components characteristics of pc with id = 798
    pc_test = Desktop()
    data_storage = HardDrive(size=152587)
    data_storage.events_one.add(BenchmarkDataStorage(read_speed=78.1, write_speed=24.4))
    cpu = Processor(cores=2, speed=2.5)
    cpu.events_one.add(BenchmarkProcessor(rate=9974.3))
    pc_test.components |= {
        data_storage,
        RamModule(size=0, speed=None),
        cpu
    }
    # add functionality and appearance range
    rate_pc = WorkbenchRate(appearance_range=AppearanceRange.B,
                            functionality_range=FunctionalityRange.A)
    # Compute all components rates and general rating
    Rate().compute(pc_test, rate_pc)

    assert round(rate_pc.ram, 2) == 1

    assert round(rate_pc.data_storage, 2) == 3.7

    assert round(rate_pc.processor, 2) == 4.09

    assert round(rate_pc.rating, 2) == 2.5
