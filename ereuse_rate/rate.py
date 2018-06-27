from ereuse_devicehub.resources.device import Computer, RamModule
from ereuse_devicehub.resources.device.models import DataStorage, Device, Processor


class BaseRate:
    def compute(self, device: Device):
        self.filtering_and_cleaning_input(device)
        self.components_parts_fusion(device)
        self.component_characteristic_normalisation(device)
        self.component_characteristic_rate(device)
        self.component_characteristic_fusion(device)

    def filtering_and_cleaning_input(self, device: Computer):
        """
        Check if input device_type is desktop or laptop.
        Get and check all the data of components are valid to prepare it
        for post calculate device score.
        """
        assert device.type == 'Desktop' or 'Laptop' or 'Server'

    def components_parts_fusion(self, device: object) -> object:
        """
        Merges all the characteristics of same type of component in one.
        For example, if we have two 100 GB disks, the result of the drive.
        size variable will be 200 GB. For example,
        if we have two RAM cards, one with 2GB and 100MB/speed,
        and the other with 4GB and 200MB/speed,
        the merger will result in a 6GB with 166MB/speed.
        """
        raise NotImplementedError()

    def component_characteristic_normalisation(self, device: Computer):
        """
        Normalise between 0 and 1 the characteristics of the components.
        We use the "Values of Characteristics" table with the values
        xMin and xMax and apply the standardisation formula,
        y = (x −xMin)/(xMax −xMin)
        """
        raise NotImplementedError()

    def component_characteristic_rate(self, device: Computer):
        """
        Apply a distribution all the scores
        The key to adapting the algorithm is that the value p = 0.242 matches
        the minimum desirable value of this characteristic.
        """
        raise NotImplementedError()

    def component_characteristic_fusion(self, device: Computer):
        """
        Established community weights and merge rate with the aesthetic and functionality scores

        """
        self.component_fusion(device)

        self.device_fusion(device)

    def component_fusion(self, device: Computer):
        """
        We do the weighted harmonic mean.
        Established community weights are 50% for processor, 20% for disk and 30% for memory.
        The result is a unique score.
        """
        raise NotImplementedError()

    def device_fusion(self, device: Computer):
        """
        Merge score with the aesthetic and functionality scores
        Score final [−2,4.7] += Score aest [−1,0.3]+ Score funct [−1,0.4]
        """
        raise NotImplementedError()


class DataStorageRate(BaseRate):

    def compute(self, device: DataStorage):
        raise NotImplementedError()

    def components_parts_fusion(self, device: object) -> object:
        raise NotImplementedError()

    def component_characteristic_normalisation(self, device: Computer):
        raise NotImplementedError()

    def component_characteristic_rate(self, device: Computer):
        raise NotImplementedError()

    def component_fusion(self, device: Computer):
        raise NotImplementedError()

    def device_fusion(self, device: Computer):
        raise NotImplementedError()


class RamRate(BaseRate):
    def compute(self, device: RamModule):
        raise NotImplementedError()

    def components_parts_fusion(self, device: object) -> object:
        raise NotImplementedError()

    def component_characteristic_normalisation(self, device: Computer):
        raise NotImplementedError()

    def component_characteristic_rate(self, device: Computer):
        raise NotImplementedError()

    def component_fusion(self, device: Computer):
        raise NotImplementedError()

    def device_fusion(self, device: Computer):
        raise NotImplementedError()


class ProcessorRate(BaseRate):
    def compute(self, device: Processor):
        raise NotImplementedError()

    def components_parts_fusion(self, device: object) -> object:
        raise NotImplementedError()

    def component_characteristic_normalisation(self, device: Computer):
        raise NotImplementedError()

    def component_characteristic_rate(self, device: Computer):
        raise NotImplementedError()

    def component_fusion(self, device: Computer):
        raise NotImplementedError()

    def device_fusion(self, device: Computer):
        raise NotImplementedError()
