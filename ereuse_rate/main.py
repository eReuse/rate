from ereuse_devicehub.resources.device.models import Device
from ereuse_devicehub.resources.enums import AggregateRatingVersions
from ereuse_devicehub.resources.event.models import AggregateRate, PhotoboxRate, Rate, \
    WorkbenchRate

from ereuse_rate.workbench import v1_0

RATE_TYPES = {
    WorkbenchRate: {
        '1.0': v1_0.Rate()
    }
}


def rate(device: Device, rate: Rate):
    """
    Rates the passed-in ``device`` and ``rate``. This method mutates
    ``rate``.
    :param device:
    :param rate: A rate with the required fields set by an agent.
    """
    cls = rate.__class__
    assert cls in RATE_TYPES, 'Rate type {} not supported.'.format(cls)
    assert str(rate.algorithm_version) in RATE_TYPES[cls], 'Rate version {} not supported.' \
                                                           ''.format(rate.algorithm_version)
    RATE_TYPES[cls][str(rate.algorithm_version)].compute(device, rate)


def aggregate_ratings(device: Device, aggregate_rate: AggregateRate):
    """
    Aggregates the ratings for the passed-in ``device`` and the
    ``aggregate_rate``. This method mutates ``aggregate_rate``.

    As for now, only version X of :class:`ereuse_devicehub.resources.
    event.models.WorkbenchRate` and version Y of :class:`ereuse_devicehub.
    resources.event.models.PhotoboxRate` are allowed.

    :param aggregate_rate: A rate with a linked
                           :class:`ereuse_devicehub.resources.event.
                           models.WorkbenchRate` or/and multiple
                           :class:`ereuse_devicehub.resources.event.
                           models.PhotoboxRate`.
    :return:
    """
    assert AggregateRatingVersions(aggregate_rate.algorithm_version) == AggregateRatingVersions.v1, \
        'This version of AggregateRating is not supported.'
    assert all(isinstance(r, (PhotoboxRate, WorkbenchRate)) for r in aggregate_rate.ratings), \
        'All rates must be a PhotoboxRate or a WorkbenchRate'
    pass