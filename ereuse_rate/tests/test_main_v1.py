from distutils.version import StrictVersion

from ereuse_devicehub.resources.device.models import Device, HardDrive, Processor, RamModule, \
    Computer
from ereuse_devicehub.resources.enums import AppearanceRange, FunctionalityRange
from ereuse_devicehub.resources.event.models import BenchmarkDataStorage, BenchmarkProcessor, \
    WorkbenchRate

from ereuse_rate import main


def test_main():
    """
    Test main rate function
    """
    pc = Computer()
    hdd = HardDrive(size=476940)
    hdd.events_one.add(BenchmarkDataStorage(read_speed=126, write_speed=29.8))
    cpu = Processor(cores=2, speed=3.4)
    cpu.events_one.add(BenchmarkProcessor(rate=27136.44))
    pc.components |= {
        hdd,
        RamModule(size=4096, speed=1600),
        RamModule(size=2048, speed=1067),
        cpu
    }
    rate = WorkbenchRate(appearance_range=AppearanceRange.A,
                         functionality_range=FunctionalityRange.A)
    # rate.algorithm_software = 'RateSoftware'
    rate.algorithm_version = StrictVersion('1.0')

    main.rate(pc, rate)
    rating_pc = 4.61

    assert float("{0:.2f}".format(rate.rating)) == rating_pc
