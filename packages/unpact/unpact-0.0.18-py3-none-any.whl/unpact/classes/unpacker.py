import itertools
from typing import Any, Dict, List, Optional, Sequence, Union

from unpact.classes.tree import Tree
from unpact.constants import MAPPING_TYPES, SEQUENCE_TYPES
from unpact.types import ColumnDef, ColumnSpec, MappingValue, SequentialValue, UnpackableData
from unpact.utils.column_defs import infer_columns
from unpact.utils.tree import create_tree


class Unpacker:
    __slots__ = ["column_defs", "allow_extra", "infer_length", "_tree"]

    def __init__(
        self,
        columns: Optional[Sequence[ColumnDef]] = None,
        allow_extra: bool = False,
        infer_length: Optional[int] = 10,
    ) -> None:
        self.allow_extra = allow_extra
        self.infer_length = infer_length
        if not columns:
            self.allow_extra = True
        self.column_defs = [ColumnSpec.from_def(c) for c in columns or []]

        self._tree: Optional[Tree] = None

    def _unwind_list(self, data: SequentialValue, tree: Tree, level_list: List, root_data: MappingValue) -> None:
        for item in data:
            item_output_dict = {}
            item_accum: List[dict] = []
            for child in tree.children:
                value: Union[dict, list] = self._unwind(item, child, root_data)
                if isinstance(value, SEQUENCE_TYPES):
                    if item_accum and len(item_accum) == len(value):  # Handle adjacents
                        item_accum = [{**a, **b} for a, b in zip(item_accum, value)]
                    else:
                        item_accum.extend(value)
                else:
                    item_output_dict.update(value)
            if len(item_accum) > 0:
                level_list.extend([{**item_output_dict, **item} for item in item_accum])
            else:
                level_list.append(item_output_dict)

    def _get_value(self, data: MappingValue, tree: Tree, root_data: MappingValue) -> Any:
        tree_data = data.get(tree.path)
        if isinstance(data, SEQUENCE_TYPES):
            return [self._unwind(d, tree, root_data) for d in data]
        if isinstance(tree_data, SEQUENCE_TYPES):
            return [tree.get_value(x, root_data, idx) for idx, x in enumerate(tree_data)]
        return tree.get_value(tree_data, root_data)

    def _unwind(
        self, data: MappingValue, tree: Tree, root_data: MappingValue
    ) -> Union[List, List[Dict[str, Any]], Dict[str, Any], dict, List[dict]]:
        if not tree.children:
            return self._get_value(data, tree, root_data)

        level_list: List[dict] = []
        level_dict: dict = {}

        tree_data = data.get(tree.path)
        tree_data = {} if tree_data is None else tree_data
        if isinstance(tree_data, SEQUENCE_TYPES):
            self._unwind_list(tree_data, tree, level_list, root_data)
        else:
            for child in tree.children:
                value = self._unwind(tree_data, child, root_data)
                if isinstance(value, SEQUENCE_TYPES):
                    level_list.extend(value)
                else:
                    level_dict.update(value)

        if len(level_list) == 0:
            return level_dict

        appended = [{**level_dict, **list_value} for list_value in level_list]
        return appended

    def apply(
        self,
        data: UnpackableData,
    ) -> List[Dict[str, Any]]:
        if not self._tree:
            self.column_defs = [ColumnSpec.from_def(c) for c in self.column_defs]
            if self.allow_extra:
                self.column_defs = infer_columns(data, self.column_defs, self.infer_length)

            self._tree = create_tree(self.column_defs)

        def apply_unwind(d: MappingValue, tree: Tree) -> List[Dict[str, Any]]:
            unwound = self._unwind({"root": d}, tree, d)
            if not isinstance(unwound, list):
                return [unwound]
            return unwound

        if isinstance(data, MAPPING_TYPES):
            return apply_unwind(data, self._tree)  # type: ignore
        else:
            return list(itertools.chain.from_iterable([apply_unwind(d, self._tree) for d in data]))  # type: ignore
