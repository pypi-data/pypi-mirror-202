import functools
import inspect
import json
import logging
import os
import sys
import warnings
from copy import deepcopy
from importlib.util import find_spec
from typing import List, Sequence

import numpy as np
import rich.syntax
import rich.tree
import torch
import wandb
from omegaconf import DictConfig, OmegaConf

from hyperbox.utils.logger import get_logger


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def _module_available(module_path: str) -> bool:
    """
    Check if a path is available in your environment

    >>> _module_available('os')
    True
    >>> _module_available('bla.bla')
    False
    """
    try:
        return find_spec(module_path) is not None
    except AttributeError:
        # Python 3.6
        return False
    except ModuleNotFoundError:
        # Python 3.7+
        return False


class TorchTensorEncoder(json.JSONEncoder):
    def default(self, o):  # pylint: disable=method-hidden
        if isinstance(o, torch.Tensor):
            olist = o.tolist()
            if "bool" not in o.type().lower() and all(map(lambda d: d == 0 or d == 1, olist)):
                print(f"Every element in {olist} is either 0 or 1. You might consider convert it into bool.")
            return olist
        return super().default(o)


def save_arch_to_json(mask: dict, filepath: str):
    with open(filepath, 'w') as f:
        json.dump(mask, f, indent=4, sort_keys=True, cls=TorchTensorEncoder)


def load_json(filename):
    if filename is None:
        data = None
    elif isinstance(filename, str):
        with open(filename, 'r') as f:
            data = json.load(f)
        for key, value in data.items():
            data[key] = torch.tensor(value)
    elif isinstance(filename, dict):
        data = filename
    else:
        raise "Wrong argument value for %s in `load_json` function" % filename
    return data


def extras(config: DictConfig) -> None:
    """A couple of optional utilities, controlled by main config file:
    - disabling warnings
    - easier access to debug mode
    - forcing debug friendly configuration

    Modifies DictConfig in place.

    Args:
        config (DictConfig): Configuration composed by Hydra.
    """

    log = get_logger()

    # enable adding new keys to config
    OmegaConf.set_struct(config, False)

    # disable python warnings if <config.ignore_warnings=True>
    if config.get("ignore_warnings"):
        log.info("Disabling python warnings! <config.ignore_warnings=True>")
        warnings.filterwarnings("ignore")

    # set <config.trainer.fast_dev_run=True> if <config.debug=True>
    if config.get("debug"):
        log.info("Running in debug mode! `trainer.fast_dev_run=True` by default! ")
        config.trainer.fast_dev_run = True

    # force debugger friendly configuration if <config.trainer.fast_dev_run=True>
    if config.trainer.get("fast_dev_run"):
        log.info("Forcing debugger friendly configuration! <config.trainer.fast_dev_run=True>")
        # Debuggers don't like GPUs or multiprocessing
        # if config.trainer.get("gpus")>1:
        #     config.trainer.gpus = 1
        # if config.datamodule.get("pin_memory"):
        #     config.datamodule.pin_memory = False
        # if config.datamodule.get("num_workers"):
        #     config.datamodule.num_workers = 0

    # backup searched network mask
    mask = config.get('model', {}).get('network_cfg', {}).get('mask', None)
    if mask:
        path = os.getcwd()
        os.system(f"cp {mask} {path}")

    # disable adding new keys to config
    OmegaConf.set_struct(config, True)


def print_config(
    config: DictConfig,
    fields: Sequence[str] = (
        "trainer",
        "model",
        "datamodule",
        "callbacks",
        "logger",
        "seed",
    ),
    resolve: bool = True,
) -> None:
    """Prints content of DictConfig using Rich library and its tree structure.

    Args:
        config (DictConfig): Configuration composed by Hydra.
        fields (Sequence[str], optional): Determines which main fields from config will
        be printed and in what order.
        resolve (bool, optional): Whether to resolve reference fields of DictConfig.
    """
    rank = os.environ.get("LOCAL_RANK", 0)
    if rank != 0:
        return
    style = "dim"
    tree = rich.tree.Tree(":gear: CONFIG", style=style, guide_style=style)

    for field in fields:
        branch = tree.add(field, style=style, guide_style=style)

        config_section = config.get(field)
        branch_content = str(config_section)
        if isinstance(config_section, DictConfig):
            branch_content = OmegaConf.to_yaml(config_section, resolve=resolve)

        branch.add(rich.syntax.Syntax(branch_content, "yaml"))

    with open("config_tree.txt", "w") as fp:
        rich.print(tree, file=fp)


def empty(*args, **kwargs):
    pass


def log_hyperparameters(
    config: DictConfig,
    model: 'pl.LightningModule',
    datamodule: 'pl.LightningDataModule',
    trainer: 'pl.Trainer',
    callbacks: 'List[pl.Callback]',
    logger: 'List[pl.loggers.LightningLoggerBase]',
) -> None:
    """This method controls which parameters from Hydra config are saved by Lightning loggers.

    Additionaly saves:
        - number of trainable model parameters
    """
    rank = os.environ.get("LOCAL_RANK", 0)
    if rank != 0:
        return

    hparams = {}

    # choose which parts of hydra config will be saved to loggers
    hparams["trainer"] = config["trainer"]
    hparams["model"] = config["model"]
    hparams["datamodule"] = config["datamodule"]
    if "seed" in config:
        hparams["seed"] = config["seed"]
    if "callbacks" in config:
        hparams["callbacks"] = config["callbacks"]

    # save number of model parameters
    hparams["model/params_total"] = sum(p.numel() for p in model.parameters())
    hparams["model/params_trainable"] = sum(
        p.numel() for p in model.parameters() if p.requires_grad
    )
    hparams["model/params_not_trainable"] = sum(
        p.numel() for p in model.parameters() if not p.requires_grad
    )

    # send hparams to all loggers
    trainer.logger.log_hyperparams(hparams)

    # disable logging any more hyperparameters for all loggers
    # this is just a trick to prevent trainer from logging hparams of model,
    # since we already did that above
    trainer.logger.log_hyperparams = empty


def finish(
    config: DictConfig,
    model: 'pl.LightningModule',
    datamodule: 'pl.LightningDataModule',
    trainer: 'pl.Trainer',
    callbacks: 'List[pl.Callback]',
    logger: 'List[pl.loggers.LightningLoggerBase]',
) -> None:
    """Makes sure everything closed properly."""

    # without this sweeps with wandb logger might crash!
    from pytorch_lightning.loggers.wandb import WandbLogger
    for lg in logger:
        if isinstance(lg, WandbLogger):
            import wandb
            wandb.finish()


def hparams_wrapper(cls):
    '''Obtain the input arguments and values of __init__ func of a class
    
        Example:
        >>> @hparams_wrapper
            class A:
                def __init__(self, a, b, c=2, d=4):
                    print(self.hparams)
        >>> a = A(2,4,5,8)
        >>> output: {'c': 5, 'd': 8, 'a': 2, 'b': 4}
    '''
    origin__new__ = deepcopy(cls.__new__)

    def __new__(cls, *args, **kwargs):
        signature = inspect.signature(cls.__init__)
        # 1. get default values of __init__ func, i.e., {'c': 2, 'd': 4} for above example
        _hparams = {
            k:v.default for k,v in signature.parameters.items() \
            if v.default is not inspect.Parameter.empty
        }
        # 2. get input arguments of __init__ func, i.e., ['a', 'b', 'c', 'd'] for above example
        _args_name = list(inspect.signature(cls.__init__).parameters.keys())[1:]
        # 3. update the default values with input arguments
        for i, arg in enumerate(args):
            _hparams[_args_name[i]] = arg
        _hparams.update(kwargs)
        # 4. create a new instance of the class
        if not isinstance(cls, type):
            self = origin__new__(type(cls))
        else:
            self = origin__new__(cls)
        self._hparams = _hparams
        # 5. set the input arguments as attributes of the class
        for key, value in self._hparams.items():
            try:
                setattr(self, key, value)
            except Exception as e:
                pass
                # print(f'{cls} `__new__` fails to set {key} to {value} due to {e}')
        if not isinstance(cls, type):
            cls = type(cls)
        cls.hparams = property(lambda self: DotDict(self._hparams)) # generate a `hparams` property function
        return self

    cls.__new__ = __new__
    return cls


def load_pretrained_weights(
    config: DictConfig, model: 'pl.LightningModule', ckpt_path: str
):
    """
    Load pretrained weights from a checkpoint.
    """
    from hydra.utils import to_absolute_path
    log = get_logger()
    # loading pretrained weight to network and mutator
    ckpt_path = to_absolute_path(config.get("pretrained_weight"))
    try:
        # load state_dict of network, mutator, and etc,.
        # model.load_state_dict(ckpt)
        model = model.load_from_checkpoint(ckpt_path, **config.model)
        log.info(f"Loading pretrained weight from {ckpt_path}, including network, mutator")
    except Exception as e:
        try:
            ckpt = torch.load(ckpt_path, map_location='cpu')
            if 'epoch' in ckpt:
                ckpt = ckpt['state_dict']
            model.load_state_dict(ckpt)
            del ckpt
            log.info(f"Loading pretrained weight from {ckpt_path}, including network")
        except Exception as e:
            try:
                # only load network weight
                model.network.load_state_dict(ckpt)
                log.info(f"Loading pretrained network weight from {ckpt_path}")
            except Exception as e:
                try:
                    # load subnet weight from a supernet weight
                    from hyperbox.networks.utils import extract_net_from_ckpt
                    weight_supernet = extract_net_from_ckpt(ckpt_path)
                    model.network.load_from_supernet(weight_supernet)
                    log.info(f"Loading subnet weight from supernet weight: {ckpt_path}")
                except Exception as e:
                    raise Exception(f'failed to load pretrained weight from {ckpt_path}.\n{e}')
    return model


def lazy_property(func):
    attr_name = "_lazy_" + func.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    return _lazy_property
