import numpy as np
import torch
import torch.nn.functional as F

from hyperbox.mutables.spaces import InputSpace, OperationSpace, ValueSpace
from hyperbox.mutator.default_mutator import Mutator
from hyperbox.mutator.random_mutator import RandomMutator


__all__ = [
    'RandomMultipleMutator',
]


class RandomMultipleMutator(RandomMutator):
    def __init__(self, model, single_path_prob=0, *args, **kwargs):
        super(RandomMultipleMutator, self).__init__(model)
        self.single_path_prob = single_path_prob

    def sample_search(self):
        if np.random.rand() < self.single_path_prob:
            return super(RandomMultipleMutator, self).sample_search()
        result = dict()
        for mutable in self.mutables:
            if isinstance(mutable, OperationSpace):
                crt_mask = torch.randint(high=2, size=(mutable.length,)).view(-1).bool()
                if crt_mask.sum() == 0:
                    crt_mask[-1] = 1
                result[mutable.key] = crt_mask.view(-1).bool()
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
