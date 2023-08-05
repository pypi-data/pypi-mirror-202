# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import torch
import torch.nn as nn
import torch.nn.functional as F

import hyperbox.mutables.spaces as spaces
from hyperbox.networks.base_nas_network import BaseNASNetwork
from .enas_ops import FactorizedReduce, StdConv, SepConvBN, Pool, ConvBranch, PoolBranch, Calibration


__all__ = [
    'Cell',
    'Node',
    'ENASMicroLayer',
    'ENASMicroNetwork',
    'ENASMacroLayer',
    'ENASMacroGeneralModel'
]


class Cell(nn.Module):
    def __init__(self, cell_name, prev_labels, channels, mask=None):
        super().__init__()
        self.input_choice = spaces.InputSpace(choose_from=prev_labels, n_chosen=1, return_mask=True,
                                                 key=cell_name + "_input", mask=mask)
        self.op_choice = spaces.OperationSpace([
            SepConvBN(channels, channels, 3, 1),
            SepConvBN(channels, channels, 5, 2),
            Pool("avg", 3, 1, 1),
            Pool("max", 3, 1, 1),
            nn.Identity()
        ], key=cell_name + "_op", mask=mask)

    def forward(self, prev_layers):
        chosen_input, chosen_mask = self.input_choice(prev_layers)
        cell_out = self.op_choice(chosen_input)
        return cell_out, chosen_mask


class Node(nn.Module):
    def __init__(self, node_name, prev_node_names, channels, mask=None):
        super().__init__()
        self.cell_x = Cell(node_name + "_x", prev_node_names, channels, mask)
        self.cell_y = Cell(node_name + "_y", prev_node_names, channels, mask)

    def forward(self, prev_layers):
        out_x, mask_x = self.cell_x(prev_layers)
        out_y, mask_y = self.cell_y(prev_layers)
        return out_x + out_y, mask_x | mask_y


class ENASMicroLayer(nn.Module):
    """
    Builtin EnasMicroLayer. Micro search designs only one building block whose architecture is repeated
    throughout the final architecture. A cell has ``num_nodes`` nodes and searches the topology and
    operations among them in RL way. The first two nodes in a layer stand for the outputs from previous
    previous layer and previous layer respectively. For the following nodes, the controller chooses
    two previous nodes and applies two operations respectively for each node. Nodes that are not served
    as input for any other node are viewed as the output of the layer. If there are multiple output nodes,
    the model will calculate the average of these nodes as the layer output. Every node's output has ``out_channels``
    channels so the result of the layer has the same number of channels as each node.

    Parameters
    ---
    num_nodes: int
        the number of nodes contained in this layer
    in_channles_pp: int
        the number of previous previous layer's output channels
    in_channels_p: int
        the number of previous layer's output channels
    out_channels: int
        output channels of this layer
    reduction: bool
        is reduction operation empolyed before this layer
    layer_id: int
        the layer id
    mask: dict
        the mask of all Mutables
    """
    def __init__(self, num_nodes, in_channels_pp, in_channels_p, out_channels, reduction, layer_id, mask):
        super().__init__()
        self.reduction = reduction
        if self.reduction:
            self.reduce0 = FactorizedReduce(in_channels_pp, out_channels, affine=False)
            self.reduce1 = FactorizedReduce(in_channels_p, out_channels, affine=False)
            in_channels_pp = in_channels_p = out_channels
        self.preproc0 = Calibration(in_channels_pp, out_channels)
        self.preproc1 = Calibration(in_channels_p, out_channels)

        self.num_nodes = num_nodes
        name_prefix = "reduce" if reduction else "normal"
        self.nodes = nn.ModuleList()
        node_labels = [spaces.InputSpace.NO_KEY, spaces.InputSpace.NO_KEY]
        for i in range(num_nodes):
            node_labels.append("layer{}_{}_node_{}".format(layer_id, name_prefix, i))
            self.nodes.append(Node(node_labels[-1], node_labels[:-1], out_channels, mask))
        self.final_conv_w = nn.Parameter(torch.zeros(out_channels, self.num_nodes + 2, out_channels, 1, 1),
                                         requires_grad=True)
        self.bn = nn.BatchNorm2d(out_channels, affine=False)
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.kaiming_normal_(self.final_conv_w)

    def forward(self, pprev, prev):
        """
        Parameters
        ---
        pprev: torch.Tensor
            the output of the previous previous layer
        prev: torch.Tensor
            the output of the previous layer
        """
        if self.reduction:
            pprev, prev = self.reduce0(pprev), self.reduce1(prev)
        pprev_, prev_ = self.preproc0(pprev), self.preproc1(prev)

        prev_nodes_out = [pprev_, prev_]
        nodes_used_mask = torch.zeros(self.num_nodes + 2, dtype=torch.bool, device=prev.device)
        for i in range(self.num_nodes):
            node_out, mask = self.nodes[i](prev_nodes_out)
            nodes_used_mask[:mask.size(0)] |= mask.to(node_out.device)
            prev_nodes_out.append(node_out)

        unused_nodes = torch.cat([out for used, out in zip(nodes_used_mask, prev_nodes_out) if not used], 1)
        unused_nodes = F.relu(unused_nodes)
        conv_weight = self.final_conv_w[:, ~nodes_used_mask, :, :, :]
        conv_weight = conv_weight.view(conv_weight.size(0), -1, 1, 1)
        out = F.conv2d(unused_nodes, conv_weight)
        return prev, self.bn(out)


class ENASMicroNetwork(BaseNASNetwork):
    def __init__(self, num_layers=2, num_nodes=5, out_channels=24, in_channels=3, num_classes=10,
                 dropout_rate=0.0, mask=None):
        super().__init__()
        self.num_layers = num_layers

        self.stem = nn.Sequential(
            nn.Conv2d(in_channels, out_channels * 3, 3, 1, 1, bias=False),
            nn.BatchNorm2d(out_channels * 3)
        )

        pool_distance = self.num_layers // 3
        pool_layers = [pool_distance, 2 * pool_distance + 1]
        self.dropout = nn.Dropout(dropout_rate)

        self.layers = nn.ModuleList()
        c_pp = c_p = out_channels * 3
        c_cur = out_channels
        for layer_id in range(self.num_layers + 2):
            reduction = False
            if layer_id in pool_layers:
                c_cur, reduction = c_p * 2, True
            self.layers.append(ENASMicroLayer(num_nodes, c_pp, c_p, c_cur, reduction, layer_id, mask))
            if reduction:
                c_pp = c_p = c_cur
            c_pp, c_p = c_p, c_cur

        self.gap = nn.AdaptiveAvgPool2d(1)
        self.dense = nn.Linear(c_cur, num_classes)

        self.reset_parameters()

    def reset_parameters(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight)

    def forward(self, x):
        bs = x.size(0)
        prev = cur = self.stem(x)
        # aux_logits = None

        for layer in self.layers:
            prev, cur = layer(prev, cur)

        cur = self.gap(F.relu(cur)).view(bs, -1)
        cur = self.dropout(cur)
        logits = self.dense(cur)

        # if aux_logits is not None:
        #     return logits, aux_logits
        return logits


class ENASMacroLayer(nn.Module):
    """
    Builtin ENAS Marco Layer. With search space changing to layer level, the controller decides
    what operation is employed and the previous layer to connect to for skip connections. The model
    is made up of the same layers but the choice of each layer may be different.

    Parameters
    ---
    key: str
        the name of this layer
    prev_labels: str
        names of all previous layers
    in_filters: int
        the number of input channels
    out_filters:
        the number of output channels
    """
    def __init__(self, key, prev_labels, in_filters, out_filters, mask=None):
        super().__init__()
        self.in_filters = in_filters
        self.out_filters = out_filters
        self.mutable = spaces.OperationSpace([
            ConvBranch(in_filters, out_filters, 3, 1, 1, separable=False),
            ConvBranch(in_filters, out_filters, 3, 1, 1, separable=True),
            ConvBranch(in_filters, out_filters, 5, 1, 2, separable=False),
            ConvBranch(in_filters, out_filters, 5, 1, 2, separable=True),
            PoolBranch('avg', in_filters, out_filters, 3, 1, 1),
            PoolBranch('max', in_filters, out_filters, 3, 1, 1)
        ], key=f"{key}_OS", mask=mask)
        if prev_labels:
            self.skipconnect = spaces.InputSpace(choose_from=prev_labels, n_chosen=None, key=f"{key}_IS", mask=mask)
        else:
            self.skipconnect = None
        self.batch_norm = nn.BatchNorm2d(out_filters, affine=False)

    def forward(self, prev_list):
        """
        Parameters
        ---
        prev_list: list
            The cell selects the last element of the list as input and applies an operation on it.
            The cell chooses none/one/multiple tensor(s) as SkipConnect(s) from the list excluding
            the last element.
        """
        out = self.mutable(prev_list[-1])
        if self.skipconnect is not None:
            connection = self.skipconnect(prev_list[:-1])
            if connection is not None:
                out += connection
        return self.batch_norm(out)


class ENASMacroGeneralModel(BaseNASNetwork):
    """
    The network is made up by stacking ENASMacroLayer. The Macro search space contains these layers.
    Each layer chooses an operation from predefined ones and SkipConnect then forms a network.

    Parameters
    ---
    num_layers: int
        The number of layers contained in the network.
    out_filters: int
        The number of each layer's output channels.
    in_channel: int
        The number of input's channels.
    num_classes: int
        The number of classes for classification.
    dropout_rate: float
        Dropout layer's dropout rate before the final dense layer.
    """
    def __init__(self, num_layers=12, out_filters=24, in_channels=3, num_classes=10,
                 dropout_rate=0.0, mask=None):
        super().__init__()
        self.num_layers = num_layers
        self.num_classes = num_classes
        self.out_filters = out_filters

        self.stem = nn.Sequential(
            nn.Conv2d(in_channels, out_filters, 3, 1, 1, bias=False),
            nn.BatchNorm2d(out_filters)
        )

        pool_distance = self.num_layers // 3
        self.pool_layers_idx = [pool_distance - 1, 2 * pool_distance - 1]
        self.dropout_rate = dropout_rate
        self.dropout = nn.Dropout(self.dropout_rate)

        self.layers = nn.ModuleList()
        self.pool_layers = nn.ModuleList()
        labels = []
        for layer_id in range(self.num_layers):
            labels.append("layer_{}".format(layer_id))
            if layer_id in self.pool_layers_idx:
                self.pool_layers.append(FactorizedReduce(self.out_filters, self.out_filters))
            self.layers.append(ENASMacroLayer(labels[-1], labels[:-1], self.out_filters, self.out_filters, mask))

        self.gap = nn.AdaptiveAvgPool2d(1)
        self.dense = nn.Linear(self.out_filters, self.num_classes)

    def forward(self, x):
        """
        Parameters
        ---
        x: torch.Tensor
            the input of the network
        """
        bs = x.size(0)
        cur = self.stem(x)

        layers = [cur]

        for layer_id in range(self.num_layers):
            cur = self.layers[layer_id](layers)
            layers.append(cur)
            if layer_id in self.pool_layers_idx:
                for i, layer in enumerate(layers):
                    layers[i] = self.pool_layers[self.pool_layers_idx.index(layer_id)](layer)
                cur = layers[-1]

        cur = self.gap(cur).view(bs, -1)
        cur = self.dropout(cur)
        logits = self.dense(cur)
        return logits
