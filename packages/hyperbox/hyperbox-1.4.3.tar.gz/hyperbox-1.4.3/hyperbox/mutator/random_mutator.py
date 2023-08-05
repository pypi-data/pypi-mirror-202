import numpy as np
import torch
import torch.nn.functional as F

from hyperbox.mutables.spaces import InputSpace, OperationSpace, ValueSpace

from hyperbox.mutator.default_mutator import Mutator

__all__ = [
    'RandomMutator',
]


class RandomMutator(Mutator):
    def __init__(self, model, *args, **kwargs):
        super().__init__(model)

    def sample_search(self):
        result = dict()
        for mutable in self.mutables:
            if isinstance(mutable, OperationSpace):
                gen_index = torch.randint(high=mutable.length, size=(1, ))
                result[mutable.key] = F.one_hot(gen_index, num_classes=mutable.length).view(-1).bool()
                mutable.mask = result[mutable.key].detach()
            elif isinstance(mutable, InputSpace):
                if mutable.n_chosen is None:
                    result[mutable.key] = torch.randint(high=2, size=(mutable.n_candidates,)).view(-1).bool()
                else:
                    perm = torch.randperm(mutable.n_candidates)
                    mask = [i in perm[:mutable.n_chosen] for i in range(mutable.n_candidates)]
                    result[mutable.key] = torch.tensor(mask, dtype=torch.bool)  # pylint: disable=not-callable
                mutable.mask = result[mutable.key].detach()
            elif isinstance(mutable, ValueSpace):
                gen_index = torch.randint(high=mutable.length, size=(1, ))
                result[mutable.key] = F.one_hot(gen_index, num_classes=mutable.length).view(-1).bool()
                mutable.mask = F.one_hot(gen_index, num_classes=mutable.length).view(-1).bool()
        return result

    def sample_final(self):
        return self.sample_search()
