from ereuse_devicehub.resources.device.models import Computer, HardDrive, RamModule, Processor
from ereuse_devicehub.resources.enums import FunctionalityRange, AppearanceRange
from ereuse_devicehub.resources.event.models import BenchmarkDataStorage, WorkbenchRate, \
    BenchmarkProcessor

from ereuse_rate.workbench.v1_0 import Rate

""" LIST DUMMIES COMPUTERS COMPONENTS CHARACTERISTICS

    pc_1193 = Computer()
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

    pc_1201 = Computer()
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

    pc_79 = Computer()
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

    pc_798 = Computer()
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
"""


def test_computer_rate():
    """
    Test Rate v1
    """
    # Create a new Computer with components characteristics of pc with id = 1193
    pc_1193 = Computer()
    hdd_1969 = HardDrive(size=476940)
    hdd_1969.events_one.add(BenchmarkDataStorage(read_speed=126, write_speed=29.8))
    cpu = Processor(cores=2, speed=3.4)
    cpu.events_one.add(BenchmarkProcessor(rate=27136.44))
    pc_1193.components |= {
        hdd_1969,
        RamModule(size=4096, speed=1600),
        RamModule(size=2048, speed=1067),
        cpu
    }
    # add functionality and appearance range
    rate_pc_1193 = WorkbenchRate(appearance_range=AppearanceRange.A,
                                 functionality_range=FunctionalityRange.A)
    # Compute all components rates and general rating
    Rate().compute(pc_1193, rate_pc_1193)

    rate_old_ram = 3.79
    assert float("{0:.2f}".format(rate_pc_1193.ram)) == rate_old_ram, \
        'Ram Rate value is not correct'

    rate_old_data_storage = 4.02
    assert float("{0:.2f}".format(rate_pc_1193.data_storage)) == rate_old_data_storage, \
        'DataStorage Rate value is not correct'

    rate_old_processor = 3.95
    assert float("{0:.2f}".format(rate_pc_1193.processor)) == rate_old_processor, \
        'Processor Rate value is not correct'

    rating = 4.61
    assert float("{0:.2f}".format(rate_pc_1193.rating)) == rating, \
        'Rate returns incorrect value(rate)'

