from distutils.version import StrictVersion
from unittest import mock
from unittest.mock import MagicMock

import pytest
import teal.currency
from ereuse_devicehub.resources.device.models import Desktop, HardDrive, Processor, \
    RamModule
from ereuse_devicehub.resources.enums import AppearanceRange, FunctionalityRange, RatingSoftware
from ereuse_devicehub.resources.event.models import AggregateRate, BenchmarkDataStorage, \
    BenchmarkProcessor, EreusePrice, WorkbenchRate

from ereuse_rate import main


def test_rate():
    """
    Test main rate function
    """
    pc = Desktop()
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
                         software=RatingSoftware.ECost,
                         version=StrictVersion('1.0'),
                         functionality_range=FunctionalityRange.A)
    rate.algorithm_version = StrictVersion('1.0')

    main.rate(pc, rate)

    assert rate.rating == 4.61


@pytest.fixture()
def app() -> MagicMock:
    """Mocks the app in ereuse event models."""
    with mock.patch('ereuse_devicehub.resources.event.models.app') as mocked_app:
        # Set default currency so app does not complain
        app.conifg = {'PRICE_CURRENCY': teal.currency.Currency.EUR}
        yield mocked_app


@pytest.mark.usefixtures('app')
def test_main():
    rate = WorkbenchRate(
        appearance_range=AppearanceRange.A,
        functionality_range=FunctionalityRange.A
    )
    pc = Desktop()
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
    rate.device = pc
    events = main.main(rate, RatingSoftware.ECost, StrictVersion('1.0'))
    price = next(e for e in events if isinstance(e, EreusePrice))
    assert price.price == 92.2
    assert price.retailer.standard.amount == 40.97
    assert price.platform.standard.amount == 18.84
    assert price.refurbisher.standard.amount == 32.38
    assert price.price >= price.retailer.standard.amount \
           + price.platform.standard.amount \
           + price.refurbisher.standard.amount
    assert price.retailer.warranty2.amount == 55.30
    assert price.platform.warranty2.amount == 25.43
    assert price.refurbisher.warranty2.amount == 43.72
    assert price.warranty2 == 124.45
    # Checks relationships
    workbench_rate = next(e for e in events if isinstance(e, WorkbenchRate))
    aggregate_rate = next(e for e in events if isinstance(e, AggregateRate))
    assert price.rating == aggregate_rate
    assert aggregate_rate.ratings[0] == workbench_rate
