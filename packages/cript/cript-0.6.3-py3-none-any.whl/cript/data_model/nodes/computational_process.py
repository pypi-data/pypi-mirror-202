from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.data import Data
from cript.data_model.nodes.experiment import Experiment
from cript.data_model.nodes.group import Group
from cript.data_model.subobjects.citation import Citation
from cript.data_model.subobjects.condition import Condition
from cript.data_model.subobjects.ingredient import Ingredient
from cript.data_model.subobjects.property import Property
from cript.data_model.subobjects.software_configuration import SoftwareConfiguration
from cript.data_model.utils import auto_assign_group

logger = getLogger(__name__)


class ComputationalProcess(BaseNode):
    """
    Object representing a simulation that processes or changes a
    virtual `Material`.
    """

    node_name = "ComputationalProcess"
    slug = "computational-process"
    alt_names = ["computational_processes"]

    @beartype
    def __init__(
        self,
        experiment: Union[Experiment, str],
        name: str,
        type: str,
        input_data: list[Union[Data, str]] = None,
        ingredients: list[Union[Ingredient, dict]] = None,
        software_configurations: list[Union[SoftwareConfiguration, dict]] = None,
        properties: list[Union[Property, dict]] = None,
        conditions: list[Union[Condition, dict]] = None,
        output_data: list[Union[Data, str]] = None,
        citations: list[Union[Citation, dict]] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        group: Union[Group, str] = None,
        **kwargs,
    ):
        super().__init__(public=public, **kwargs)
        self.experiment = experiment
        self.name = name
        self.type = type
        self.input_data = input_data if input_data else []
        self.ingredients = ingredients if ingredients else []
        self.software_configurations = (
            software_configurations if software_configurations else []
        )
        self.properties = properties if properties else []
        self.conditions = conditions if conditions else []
        self.output_data = output_data if output_data else []
        self.citations = citations if citations else []
        self.notes = notes
        self.group = auto_assign_group(group, experiment)

    @beartype
    def add_input_data(self, data: Union[Data, dict]):
        self._add_node(data, "input_data")

    @beartype
    def remove_input_data(self, data: Union[Data, int]):
        self._remove_node(data, "input_data")

    @beartype
    def add_ingredient(self, ingredient: Union[Ingredient, dict]):
        self._add_node(ingredient, "ingredients")

    @beartype
    def remove_ingredient(self, ingredient: Union[Ingredient, int]):
        self._remove_node(ingredient, "ingredients")

    @beartype
    def add_software_configuration(
        self, configuration: Union[SoftwareConfiguration, dict]
    ):
        self._add_node(configuration, "software_configurations")

    @beartype
    def remove_software_configurations(
        self, configuration: Union[SoftwareConfiguration, int]
    ):
        self._remove_node(configuration, "software_configurations")

    @beartype
    def add_property(self, property: Union[Property, dict]):
        self._add_node(property, "properties")

    @beartype
    def remove_property(self, property: Union[Property, int]):
        self._remove_node(property, "properties")

    @beartype
    def add_condition(self, condition: Union[Condition, dict]):
        self._add_node(condition, "conditions")

    @beartype
    def remove_condition(self, condition: Union[Condition, int]):
        self._remove_node(condition, "conditions")

    @beartype
    def add_output_data(self, data: Union[Data, dict]):
        self._add_node(data, "output_data")

    @beartype
    def remove_output_data(self, data: Union[Data, int]):
        self._remove_node(data, "output_data")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")
