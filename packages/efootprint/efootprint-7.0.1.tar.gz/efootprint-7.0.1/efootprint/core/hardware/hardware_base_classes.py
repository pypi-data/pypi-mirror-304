from abc import abstractmethod
from typing import List

from efootprint.abstract_modeling_classes.explainable_objects import ExplainableQuantity
from efootprint.abstract_modeling_classes.modeling_object import ModelingObject
from efootprint.constants.sources import Sources, SOURCE_VALUE_DEFAULT_NAME
from efootprint.abstract_modeling_classes.source_objects import SourceValue
from efootprint.constants.units import u


class Hardware(ModelingObject):
    def __init__(self, name: str, carbon_footprint_fabrication: SourceValue, power: SourceValue,
                 lifespan: SourceValue, fraction_of_usage_time: SourceValue):
        super().__init__(name)
        self.carbon_footprint_fabrication = carbon_footprint_fabrication.set_label(
            f"Carbon footprint fabrication of {self.name}")
        self.power = power.set_label(f"Power of {self.name}")
        self.lifespan = lifespan.set_label(f"Lifespan of {self.name}")
        if not fraction_of_usage_time.value.check("[]"):
            raise ValueError("Variable 'fraction_of_usage_per_day' shouldn’t have any dimensionality")
        self.fraction_of_usage_time = fraction_of_usage_time.set_label(f"{self.name} fraction of usage time")

    @property
    def modeling_objects_whose_attributes_depend_directly_on_me(self) -> List[ModelingObject]:
        return self.modeling_obj_containers

    @property
    def systems(self) -> List:
        return list(set(sum([mod_obj.systems for mod_obj in self.modeling_obj_containers], start=[])))


class InfraHardware(Hardware):
    def __init__(self, name: str, carbon_footprint_fabrication: SourceValue, power: SourceValue, lifespan: SourceValue,
                 average_carbon_intensity: SourceValue):
        super().__init__(
            name, carbon_footprint_fabrication, power, lifespan, SourceValue(1 * u.dimensionless, Sources.HYPOTHESIS))
        self.raw_nb_of_instances = None
        self.nb_of_instances = None
        self.instances_energy = None
        self.energy_footprint = None
        self.instances_fabrication_footprint = None
        if not average_carbon_intensity.value.check("[time]**2 / [length]**2"):
            raise ValueError(
                "Variable 'average_carbon_intensity' does not have mass over energy "
                "('[time]**2 / [length]**2') dimensionality"
            )
        self.average_carbon_intensity = average_carbon_intensity
        if self.average_carbon_intensity.label == SOURCE_VALUE_DEFAULT_NAME:
            self.average_carbon_intensity.set_label(f"Average carbon intensity of {self.name} electricity")

    @property
    def modeling_objects_whose_attributes_depend_directly_on_me(self) -> List:
        return []

    @abstractmethod
    def update_raw_nb_of_instances(self):
        pass

    @abstractmethod
    def update_nb_of_instances(self):
        pass

    @abstractmethod
    def update_instances_energy(self):
        pass

    @property
    def jobs(self):
        return self.modeling_obj_containers

    @property
    def systems(self) -> List:
        return list(set(sum([job.systems for job in self.jobs], start=[])))

    def update_instances_fabrication_footprint(self):
        instances_fabrication_footprint = (
                self.carbon_footprint_fabrication * self.nb_of_instances * ExplainableQuantity(1 * u.hour, "one hour")
                / self.lifespan)

        self.instances_fabrication_footprint = instances_fabrication_footprint.to(u.kg).set_label(
                f"Hourly {self.name} instances fabrication footprint")

    def update_energy_footprint(self):
        energy_footprint = (self.instances_energy * self.average_carbon_intensity)

        self.energy_footprint = energy_footprint.to(u.kg).set_label(f"Hourly {self.name} energy footprint")
