from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.experiment import Experiment
from cript.data_model.nodes.group import Group
from cript.data_model.nodes.material import Material
from cript.data_model.subobjects.citation import Citation
from cript.data_model.subobjects.condition import Condition
from cript.data_model.subobjects.equipment import Equipment
from cript.data_model.subobjects.ingredient import Ingredient
from cript.data_model.subobjects.property import Property
from cript.data_model.utils import auto_assign_group

logger = getLogger(__name__)


class Process(BaseNode):
    """
    Object representing a process of creating or transforming
    a `Material` object.
    """

    node_name = "Process"
    slug = "process"
    alt_names = ["processes", "prerequisite_processes", "sample_preparation"]

    @beartype
    def __init__(
        self,
        experiment: Union[Experiment, str],
        name: str,
        type: str,
        keywords: Union[list[str], None] = None,
        description: Union[str, None] = None,
        prerequisite_processes: list[Union[BaseNode, str]] = None,
        ingredients: list[Union[Ingredient, dict]] = None,
        equipment: list[Union[Equipment, dict]] = None,
        properties: list[Union[Property, dict]] = None,
        conditions: list[Union[Condition, dict]] = None,
        set_id: Union[int, None] = None,
        products: list[Union[Material, str]] = None,
        waste: list[Union[Material, str]] = None,
        citations: list[Union[Citation, dict]] = None,
        public: bool = False,
        group: Union[Group, str] = None,
        **kwargs,
    ):
        super().__init__(public=public, **kwargs)
        self.experiment = experiment
        self.name = name
        self.type = type
        self.keywords = keywords if keywords else []
        self.description = description
        self.prerequisite_processes = (
            prerequisite_processes if prerequisite_processes else []
        )
        self.ingredients = ingredients if ingredients else []
        self.equipment = equipment if equipment else []
        self.properties = properties if properties else []
        self.conditions = conditions if conditions else []
        self.set_id = set_id
        self.products = products if products else []
        self.waste = waste if waste else []
        self.citations = citations if citations else []
        self.group = auto_assign_group(group, experiment)

    @beartype
    def add_equipment(self, piece: Union[Equipment, dict]):
        self._add_node(piece, "equipment")

    @beartype
    def remove_equipment(self, piece: Union[Equipment, int]):
        self._remove_node(piece, "equipment")

    @beartype
    def add_prerequisite_process(self, process: Union[BaseNode, dict]):
        self._add_node(process, "prerequisite_processes")

    @beartype
    def remove_prerequisite_process(self, process: Union[BaseNode, int]):
        self._remove_node(process, "prerequisite_processes")

    @beartype
    def add_ingredient(self, ingredient: Union[Ingredient, dict]):
        self._add_node(ingredient, "ingredients")

    @beartype
    def remove_ingredient(self, ingredient: Union[Ingredient, int]):
        self._remove_node(ingredient, "ingredients")

    @beartype
    def add_product(self, material: Union[Material, dict]):
        self._add_node(material, "products")

    @beartype
    def remove_product(self, material: Union[Material, int]):
        self._remove_node(material, "products")

    @beartype
    def add_waste(self, material: Union[Material, dict]):
        self._add_node(material, "waste")

    @beartype
    def remove_waste(self, material: Union[Material, int]):
        self._remove_node(material, "waste")

    @beartype
    def add_condition(self, condition: Union[Condition, dict]):
        self._add_node(condition, "conditions")

    @beartype
    def remove_condition(self, condition: Union[Condition, int]):
        self._remove_node(condition, "conditions")

    @beartype
    def add_property(self, property: Union[Property, dict]):
        self._add_node(property, "properties")

    @beartype
    def remove_property(self, property: Union[Property, int]):
        self._remove_node(property, "properties")

    @beartype
    def add_citation(self, citation: Union[Citation, dict]):
        self._add_node(citation, "citations")

    @beartype
    def remove_citation(self, citation: Union[Citation, int]):
        self._remove_node(citation, "citations")
