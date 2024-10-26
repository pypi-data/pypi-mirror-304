from __future__ import annotations
from collections import defaultdict
from typing import Any, Callable, Dict, List, Tuple, Union


class GenericTree(defaultdict):
    """
    A generic tree data structure where each node can be either an internal node
    with child nodes or a leaf node containing a value. Leaf nodes store their
    value under a special key '_value'.
    """

    _LEAF_KEY = '_value'

    def __init__(self, *args, **kwargs):
        """
        Initialize the GenericTree. It acts as a defaultdict where missing keys
        create new GenericTree instances.
        """
        super().__init__(self.__class__, *args, **kwargs)

    def __getitem__(self, key):
        """
        Get the child node or value associated with the given key.

        - If the current node is a leaf and the key is '_value', returns the value.
        - If the current node is a leaf and the key is not '_value', raises KeyError.
        - If the child node is a leaf, returns its value.
        - Otherwise, returns the child node.
        """
        if self.is_leaf():
            if key == self._LEAF_KEY:
                return super().__getitem__(key)
            else:
                raise KeyError(f'Leaf node has no key "{key}".')
        else:
            child = super().__getitem__(key)
            if child.is_leaf():
                return child.get_value()
            else:
                return child

    def __setitem__(self, key, value):
        """
        Set the child node or value associated with the given key.

        - If the current node is a leaf, can only set '_value'.
        - If setting '_value' on an internal node, only allowed if the node has no other keys.
        - If the value is a GenericTree instance, sets it as the child node.
        - Otherwise, creates a leaf node with the given value.
        """
        if self.is_leaf():
            if key == self._LEAF_KEY:
                super().__setitem__(key, value)
            else:
                raise KeyError(f'Cannot set key "{key}" on a leaf node.')
        else:
            if key == self._LEAF_KEY:
                if not self.keys():
                    super().__setitem__(key, value)
                else:
                    raise KeyError(f'Cannot set a value on a non-empty internal node.')
            else:
                if isinstance(value, GenericTree):
                    super().__setitem__(key, value)
                else:
                    super().__setitem__(key, self.__class__.leaf(value))

    def add(self, path: Tuple[str, ...], value: Any):
        """
        Add a value to the tree at the specified path.

        Parameters:
        - path: A tuple of keys representing the path.
        - value: The value to set at the path.

        Raises:
        - ValueError: If attempting to add to a leaf node.
        """
        if self.is_leaf():
            raise ValueError('Cannot add to a leaf node.')
        tree = self
        for part in path:
            tree = tree[part]
        tree.set_value(value)

    def lookup(self, path: Tuple[str, ...]) -> Union[GenericTree, Any]:
        """
        Retrieve the value or subtree at the specified path.

        Parameters:
        - path: A tuple of keys representing the path.

        Returns:
        - The value if the node at the path is a leaf.
        - The subtree if the node at the path is an internal node.
        """
        if self.is_leaf() and len(path) == 0:
            return self.get_value()
        tree = self
        for part in path:
            tree = tree[part]
        return tree

    def filter(self, path_filters: List[Union[None, List[str]]]) -> GenericTree:
        """
        Filter the tree based on the provided path filters.

        Parameters:
        - path_filters: A list where each element is either None or a list of keys.
          None means all keys at that level are included.

        Returns:
        - A new GenericTree containing only the filtered paths.

        Raises:
        - ValueError: If a specified key is not found.
        """
        if self.is_leaf() or not path_filters:
            return self.copy()

        keys = path_filters[0]
        if keys is None:
            keys = list(self.keys())
        new_tree = self.__class__()
        for key in keys:
            if key not in self:
                raise ValueError(f'Key "{key}" not found in the tree.')
            value = self[key]
            if not isinstance(value, self.__class__):
                new_tree[key] = self.__class__.leaf(value)
            else:
                new_tree[key] = self[key].filter(path_filters[1:])
        return new_tree

    def prune(self) -> GenericTree:
        """
        Simplify the tree by removing levels that contain only a single child.

        Returns:
        - A new pruned GenericTree.
        """
        if self.is_leaf():
            return self.copy()

        new_tree = self.__class__()
        for key, value in self.items():
            new_value = value.prune()
            if len(new_value) == 1 and not new_value.is_leaf():
                # Replace the node with its single child
                child_key = next(iter(new_value.keys()))
                new_tree[key] = new_value[child_key]
            else:
                new_tree[key] = new_value

        # If the new tree has only one child and is not a leaf, return that child
        if len(new_tree) == 1 and not new_tree.is_leaf():
            return next(iter(new_tree.values()))

        return new_tree

    def map(self, func: Callable[[Any], Any]) -> GenericTree:
        """
        Apply a function to all values in the tree.

        Parameters:
        - func: A function that takes a value and returns a new value.

        Returns:
        - A new GenericTree with the function applied to all values.
        """
        if self.is_leaf():
            return self.__class__.leaf(func(self.get_value()))
        new_tree = self.__class__()
        for key, value in self.items():
            new_tree[key] = value.map(func)
        return new_tree

    def pretty_print(self, level=0):
        """
        Print the tree in a human-readable format.

        Parameters:
        - level: The current indentation level (used internally for recursion).
        """
        indent = '    ' * level
        if level == 0:
            print(f'{self.__class__.__name__}[')
        if self.is_leaf():
            print(f'{indent} = {self.get_value()}')
        else:
            for key, value in self.items():
                print(f'{indent}{key}:')
                value.pretty_print(level=level + 1)
        if level == 0:
            print(']')

    def is_leaf(self) -> bool:
        """
        Check if the node is a leaf node.

        Returns:
        - True if the node is a leaf, False otherwise.
        """
        return self._LEAF_KEY in self

    def num_children(self) -> int:
        """
        Get the number of child nodes.

        Returns:
        - The number of children, excluding the '_value' key if present.
        """
        return len(self) - int(self.is_leaf())

    def get_value(self) -> Any:
        """
        Get the value of a leaf node.

        Returns:
        - The value stored in the leaf node.

        Raises:
        - KeyError: If the node is not a leaf.
        """
        if self.is_leaf():
            return self[self._LEAF_KEY]
        else:
            raise KeyError('Cannot get value from a non-leaf node.')

    def set_value(self, value: Any):
        """
        Set the value of a node, making it a leaf node.

        Parameters:
        - value: The value to set.

        Raises:
        - ValueError: If the node has existing children and is not a leaf.
        """
        if self.keys() and not self.is_leaf():
            raise ValueError('Cannot set value of a non-leaf node with children.')
        self[self._LEAF_KEY] = value

    @classmethod
    def leaf(cls, value: Any) -> GenericTree:
        """
        Create a leaf node with the given value.

        Parameters:
        - value: The value to store in the leaf node.

        Returns:
        - A new GenericTree instance representing a leaf node.
        """
        leaf = cls()
        leaf.set_value(value)
        return leaf

    def __eq__(self, other: GenericTree) -> bool:
        """
        Check if two trees are equal.

        Parameters:
        - other: The other GenericTree to compare.

        Returns:
        - True if the trees are equal, False otherwise.
        """
        if not isinstance(other, GenericTree):
            return False
        if self.is_leaf() != other.is_leaf():
            return False
        if self.is_leaf():
            return self.get_value() == other.get_value()
        if set(self.keys()) != set(other.keys()):
            return False
        return all(self[key] == other[key] for key in self.keys())

    def __copy__(self) -> GenericTree:
        """
        Create a shallow copy of the tree.

        Returns:
        - A new GenericTree instance that is a copy of the current tree.
        """
        if self.is_leaf():
            return self.__class__.leaf(self.get_value())
        new_tree = self.__class__()
        for key, value in self.items():
            new_tree[key] = value.__copy__()
        return new_tree

    copy = __copy__

    def __str__(self) -> str:
        """
        Get a string representation of the tree.

        Returns:
        - A string representing the tree structure.
        """
        if self.is_leaf():
            return f'{self.__class__.__name__}[{self._LEAF_KEY} = {self.get_value()}]'
        else:
            keys = ', '.join(f'"{key}"' for key in self.keys())
            return f'{self.__class__.__name__}[{keys}]'

    __repr__ = __str__

