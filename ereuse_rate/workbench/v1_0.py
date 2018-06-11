from ereuse_devicehub.resources.device.models import Computer, DataStorage

from ereuse_rate.rate import BaseRate, _DataStorageRate


class Rate(BaseRate):
    def compute(self, device: Computer):
        # todo Call all scores of components
        for component in device.components:
            pass
        # todo make something with all scores
        # todo return scores
        self.filtering_and_cleaning(device)
        self.components_parts_fusion(device)
        self.component_characteristic_normalisation(device)
        self.component_characteristic_rate(device)

    def filtering_and_cleaning_input(self, device: Computer):
        pass

    def components_parts_fusion(self, device: object) -> object:
        return super().components_parts_fusion(device)

    def component_characteristic_normalisation(self, device: Computer):
        super().component_characteristic_normalisation(device)

    def component_characteristic_rate(self, device: Computer):
        super().component_characteristic_rate(device)

    def component_fusion(self, device: Computer):
        super().component_fusion(device)

    def device_fusion(self, device: Computer):
        super().device_fusion(device)


class DataStorageRate(_DataStorageRate):
    def filtering_and_cleaning_input(self, device: Computer):
        pass

    READING_SPEED_MIN = 2.7
    READING_SPEED_MAX = 109.5
    WRITING_SPEED_MIN = 2
    WRITING_SPEED_MAX = 27.35

    def compute(self, device: DataStorage):
        pass
