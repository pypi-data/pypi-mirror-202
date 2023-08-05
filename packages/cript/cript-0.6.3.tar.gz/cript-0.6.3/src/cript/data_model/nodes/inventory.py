from logging import getLogger
from typing import Union

from beartype import beartype

from cript.data_model.nodes.base_node import BaseNode
from cript.data_model.nodes.collection import Collection
from cript.data_model.nodes.group import Group
from cript.data_model.nodes.material import Material
from cript.data_model.utils import auto_assign_group

logger = getLogger(__name__)


class Inventory(BaseNode):
    """Object representing a logical grouping of `Material` objects."""

    node_name = "Inventory"
    slug = "inventory"

    @beartype
    def __init__(
        self,
        collection: Union[Collection, str],
        name: str,
        materials: list[Union[Material, str]] = None,
        notes: Union[str, None] = None,
        public: bool = False,
        group: Union[Group, str] = None,
        **kwargs,
    ):
        super().__init__(public=public, **kwargs)
        self.collection = collection
        self.name = name
        self.notes = notes
        self.materials = materials if materials else []
        self.group = auto_assign_group(group, collection)

        self.__index_table = dict()
        self.__degenerate_index_table = set()

    def __getitem__(self, obj: Union[int, slice, str]) -> Material:
        """
        obj can be an index or slice of self.materials or a unique identifier of a material
        """
        if isinstance(obj, (int, slice)):
            return self.materials[obj]
        elif isinstance(obj, str):
            if not self.__index_table:
                self._generate_index_table()
            if obj in self.__index_table:
                return self.materials[self.__index_table[obj]]
            if obj in self.__degenerate_index_table:
                raise ValueError("Multiple materials share this index. Try another.")
            raise ValueError(
                f"'{obj}' not found in Inventory: {self.name}."
                " (exact match required, case sensitive)"
            )

        raise TypeError("Invalid object for indexing.")

    def __len__(self) -> int:
        return len(self.materials)

    def __iter__(self) -> list[Material]:
        return self.materials

    @beartype
    def add_material(self, material: Union[Material, dict]):
        self._add_node(material, "materials")

    @beartype
    def remove_material(self, material: Union[Material, int]):
        self._remove_node(material, "materials")

    def _generate_index_table(self):
        for i, material in enumerate(self.materials):
            self._add_value_index_table(material.name, i)
            self._add_value_index_table(material.uid, i)
            for identifier in material.identifiers:
                if isinstance(identifier.value, list):
                    for value in identifier.value:
                        self._add_value_index_table(value, i)
                else:
                    self._add_value_index_table(identifier.value, i)

    def _add_value_index_table(self, value: str, index: int):
        if value in self.__index_table:
            if self.__index_table[value] != index:
                # if value is already in index table and not from same material node,
                # remove it and add to degenerate table
                del self.__index_table[value]
                self.__degenerate_index_table.add(value)
            return

        self.__index_table[value] = index
