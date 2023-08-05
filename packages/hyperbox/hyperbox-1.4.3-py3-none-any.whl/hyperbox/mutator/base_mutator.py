# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import logging

import torch.nn as nn

from hyperbox.mutables.spaces import Mutable, MutableScope, InputSpace


class StructuredMutableTreeNode:
    """
    A structured representation of a search space.
    A search space comes with a root (with `None` stored in its `mutable`), and a bunch of children in its `children`.
    This tree can be seen as a "flattened" version of the module tree. Since nested mutable entity is not supported yet,
    the following must be true: each subtree corresponds to a ``MutableScope`` and each leaf corresponds to a
    ``Mutable`` (other than ``MutableScope``).
    """

    def __init__(self, mutable, order='pre', deduplicate=True):
        self.mutable = mutable
        self.order = order
        self.deduplicate = deduplicate
        self.children = []

    def add_child(self, mutable):
        self.children.append(StructuredMutableTreeNode(mutable))
        return self.children[-1]

    def type(self):
        return type(self.mutable)

    def __iter__(self):
        return self.traverse(order=self.order, deduplicate=self.deduplicate)

    def traverse(self, order="pre", deduplicate=True, memo=None):
        """
        Return a generator that generates a list of mutables in this tree.

        Parameters
        ----------
        order : str
            pre or post. If pre, current mutable is yield before children. Otherwise after.
        deduplicate : bool
            If true, mutables with the same key will not appear after the first appearance.
        memo : dict
            An auxiliary dict that memorize keys seen before, so that deduplication is possible.

        Returns
        -------
        generator of Mutable
        """
        if memo is None:
            memo = set()
        assert order in ["pre", "post"]
        if order == "pre":
            if self.mutable is not None:
                if not deduplicate or self.mutable.key not in memo:
                    memo.add(self.mutable.key)
                    yield self.mutable
        for child in self.children:
            for m in child.traverse(order=order, deduplicate=deduplicate, memo=memo):
                yield m
        if order == "post":
            if self.mutable is not None:
                if not deduplicate or self.mutable.key not in memo:
                    memo.add(self.mutable.key)
                    yield self.mutable


class BaseMutator(nn.Module):
    """
    A mutator is responsible for mutating a graph by obtaining the search space from the network and implementing
    callbacks that are called in ``forward`` in Mutables.
    """
    ORDER = 'pre'
    DEDUPLICATE = True

    def __init__(self, model):
        super().__init__()
        self.order = self.ORDER
        self.deduplicate = self.DEDUPLICATE
        self.__dict__["model"] = model
        self._structured_mutables = self._parse_search_space(self.model)

    def _parse_search_space(self, module, root=None, prefix="", memo=None, nested_detection=None):
        if memo is None:
            memo = set()
        if root is None:
            root = StructuredMutableTreeNode(None, order=self.order, deduplicate=self.deduplicate)
        if module not in memo:
            memo.add(module)
            if isinstance(module, Mutable):
                if nested_detection is not None:
                    raise RuntimeError("Cannot have nested search space. Error at {} in {}"
                                       .format(module, nested_detection))
                module.name = prefix
                module.set_mutator(self)
                root = root.add_child(module)
                if not isinstance(module, MutableScope):
                    nested_detection = module
                # if isinstance(module, InputSpace):
                #     for k in module.choose_from:
                #         if k != InputSpace.NO_KEY and k not in [m.key for m in memo if isinstance(m, Mutable)]:
                #             raise RuntimeError("'{}' required by '{}' not found in keys that appeared before, and is not NO_KEY."
                #                                .format(k, module.key))
            for name, submodule in module._modules.items():
                if submodule is None:
                    continue
                submodule_prefix = prefix + ("." if prefix else "") + name
                self._parse_search_space(submodule, root, submodule_prefix, memo=memo,
                                         nested_detection=nested_detection)
        return root

    @property
    def mutables(self):
        return self._structured_mutables

    def forward(self, *inputs):
        raise RuntimeError("Forward is undefined for mutators.")

    def __setattr__(self, name, value):
        if name == "model":
            raise AttributeError("Attribute `model` can be set at most once, and you shouldn't use `self.model = model` to "
                                 "include you network, as it will include all parameters in model into the mutator.")
        return super().__setattr__(name, value)

    def enter_mutable_scope(self, mutable_scope):
        """
        Callback when forward of a MutableScope is entered.

        Parameters
        ----------
        mutable_scope : MutableScope
        """
        pass

    def exit_mutable_scope(self, mutable_scope):
        """
        Callback when forward of a MutableScope is exited.

        Parameters
        ----------
        mutable_scope : MutableScope
        """
        pass

    def on_forward_operation_space(self, mutable, *inputs):
        """
        Callbacks of forward in OperationSpace.

        Parameters
        ----------
        mutable : OperationSpace
        inputs : list of torch.Tensor

        Returns
        -------
        tuple of torch.Tensor and torch.Tensor
            output tensor and mask
        """
        raise NotImplementedError

    def on_forward_input_space(self, mutable, tensor_list):
        """
        Callbacks of forward in InputSpace.

        Parameters
        ----------
        mutable : InputSpace
        tensor_list : list of torch.Tensor

        Returns
        -------
        tuple of torch.Tensor and torch.Tensor
            output tensor and mask
        """
        raise NotImplementedError

    def export(self):
        """
        Export the data of all decisions. This should output the decisions of all the mutables, so that the whole
        network can be fully determined with these decisions for further training from scratch.

        Returns
        -------
        dict
        """
        raise NotImplementedError
