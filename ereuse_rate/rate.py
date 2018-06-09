from ereuse_devicehub.resources.device.models import DataStorage, Device


class BaseScore:
    def compute(self, device: Device):
        raise NotImplementedError()


class DataStorageScore(BaseScore):
    def compute(self, device: DataStorage):
        raise NotImplementedError()
