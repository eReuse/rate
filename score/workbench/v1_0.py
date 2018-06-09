from ereuse_devicehub.resources.device.models import Computer, DataStorage

from score.rate import BaseScore, DataStorageScore as _DataStorageScore


class Score(BaseScore):
    def compute(self, device: Computer):
        # todo Call all scores of components
        for component in device.components:
            pass
        # todo make something with all scores
        # todo return scores


class DataStorageScore(_DataStorageScore):
    READING_SPEED_MIN = 2.7
    READING_SPEED_MAX = 109.5
    WRITING_SPEED_MIN = 2
    WRITING_SPEED_MAX = 27.35

    def compute(self, device: DataStorage):
        pass
