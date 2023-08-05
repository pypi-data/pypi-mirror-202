from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.material import Material
from cript.data_model.subobjects.base_subobject import BaseSubobject
from cript.data_model.subobjects.quantity import Quantity

logger = getLogger(__name__)


class Ingredient(BaseSubobject):
    """
    Object representing a `Material` object being used
    as an input to a `Process` object.
    """

    node_name = "Ingredient"
    alt_names = ["ingredients"]

    @beartype
    def __init__(
        self,
        material: Union[Material, str],
        quantities: list[Union[Quantity, dict]],
        keyword: str = None,
    ):
        super().__init__()
        self.material = material
        self.keyword = keyword
        self.quantities = quantities if quantities else []

    @beartype
    def add_quantity(self, quantity: Union[Quantity, dict]):
        self._add_node(quantity, "quantities")

    @beartype
    def remove_quantity(self, quantity: Union[Quantity, int]):
        self._remove_node(quantity, "quantities")
