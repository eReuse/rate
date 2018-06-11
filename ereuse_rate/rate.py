from ereuse_devicehub.resources.device.models import DataStorage, Device


class BaseScore:
    def compute(self, device: Device):
        raise NotImplementedError()

    def filtering_and_cleaning_input(self, device: Computer):
        """
        Check if input device_type is desktop or laptop.
        Get and check all the data of components are valid to prepare it
        for post calculate device score.
        """
        raise NotImplementedError()

    def components_parts_fusion(self, device: object) -> object:
        """
        Merges all the characteristics of same type of component in one.
        For example, if we have two 100 GB disks, the result of the drive.
        size variable will be 200 GB. For example,
        if we have two RAM cards, one with 2GB and 100MB/speed,
        and the other with 4GB and 200MB/speed,
        the merger will result in a 6GB with 166MB/speed.
        """
        pass

    def component_characteristic_normalisation(self, device: Computer):
        """
        Normalise between 0 and 1 the characteristics of the components.
        We use the "Values of Characteristics" table with the values
        xMin and xMax and apply the standardisation formula,
        y = (x −xMin)/(xMax −xMin)
        """

    def component_characteristic_rate(self, device: Computer):
        """
        Apply a distribution all the scores
        The key to adapting the algorithm is that the value p = 0.242 matches
        the minimum desirable value of this characteristic.
        """

    def component_characteristic_fusion(self, device: Computer):
        """
        Established community weights and merge rate with the aesthetic and functionality scores

        """
        component_fusion((self, device: Computer)

        device_fusion((self, device: Computer)

    def component_fusion(self, device: Computer):
        """
        We do the weighted harmonic mean.
        Established community weights are 50% for processor, 20% for disk and 30% for memory.
        The result is a unique score.
        """

    def device_fusion(self, device: Computer):
        """
         Merge score with the aesthetic and functionality scores
         Score final [−2,4.7] += Score aest [−1,0.3]+ Score funct [−1,0.4]
        """


class DataStorageScore(BaseScore):
    def compute(self, device: DataStorage):
        raise NotImplementedError()
