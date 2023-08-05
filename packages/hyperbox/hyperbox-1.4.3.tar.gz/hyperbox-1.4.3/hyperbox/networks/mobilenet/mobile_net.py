import torch
import torch.nn as nn
import math

from hyperbox.mutables.spaces import OperationSpace
from hyperbox.utils.utils import load_json

from hyperbox.networks.base_nas_network import BaseNASNetwork
from hyperbox.networks.mobilenet.mobile_ops import *
from hyperbox.networks.mobilenet.mobile_utils import *


class MobileNet(BaseNASNetwork):
    OP_LIST = ['3x3_MBConv3', '3x3_MBConv6', '5x5_MBConv3', '5x5_MBConv6',
        '7x7_MBConv3', '7x7_MBConv6', 'Identity', 'Zero']

    def __init__(
        self,
        c_in: int=3,
        first_stride: int=1,
        width_stages: list=[24,40,80,96,192,320],
        n_cell_stages: list=[4,4,4,4,4,1],
        stride_stages: list=[2,2,2,1,2,1],
        op_list: list = None,
        width_mult: int=1,
        classes: int=1000,
        dropout_rate: float=0,
        bn_param: tuple=(0.1, 1e-3),
        mask: dict=None
    ):
        """
        Parameters
            ----------
            width_stages: str
                width (output channels) of each cell stage in the block
            n_cell_stages: str
                number of cells in each cell stage
            stride_strages: str
                stride of each cell stage in the block
            width_mult : int
                the scale factor of width
        """
        super(MobileNet, self).__init__(mask)
        if op_list is None:
            self.op_list = self.OP_LIST 
        else:
            self.op_list = op_list
        input_channel = make_divisible(32 * width_mult, 8)
        first_cell_width = make_divisible(16 * width_mult, 8)
        for i in range(len(width_stages)):
            width_stages[i] = make_divisible(width_stages[i] * width_mult, 8)

        # first conv
        first_conv = ConvLayer(c_in, input_channel, kernel_size=3, stride=first_stride, use_bn=True, act_func='relu6', ops_order='weight_bn_act')

        # first block
        first_block = OPS['3x3_MBConv1'](input_channel, first_cell_width, 1)
        input_channel = first_cell_width
        blocks = [first_block]

        stage_cnt = 0
        for width, n_cell, s in zip(width_stages, n_cell_stages, stride_stages):
            for i in range(n_cell):
                if i == 0:
                    stride = s
                else:
                    stride = 1
                calibrate_op = CalibrationLayer(input_channel, width, stride)
                blocks.append(calibrate_op)
                op_candidates = [OPS[op](width, width, 1) for op in self.op_list]
                conv_op = OperationSpace(op_candidates, return_mask=True, key="s{}_c{}".format(stage_cnt, i), mask=self.mask)
                # shortcut
                if stride == 1 and input_channel == width:
                    # if not first cell
                    shortcut = IdentityLayer(input_channel, input_channel)
                else:
                    shortcut = None
                inverted_residual_block = MobileInvertedResidualBlock(conv_op, shortcut, op_candidates)
                blocks.append(inverted_residual_block)
                input_channel = width
            stage_cnt += 1

        # feature mix layer
        last_channel = make_devisible(1280 * width_mult, 8) if width_mult > 1.0 else 1280
        feature_mix_layer = ConvLayer(input_channel, last_channel, kernel_size=1, use_bn=True, act_func='relu6', ops_order='weight_bn_act', )
        classifier = LinearLayer(last_channel, classes, dropout_rate=dropout_rate)

        self.first_conv = first_conv
        self.blocks = nn.Sequential(*blocks)
        self.feature_mix_layer = feature_mix_layer
        self.global_avg_pooling = torch.nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(1) # same as x.view(x.size(0), -1)
        )
        self.classifier = classifier

        # set bn param
        self.set_bn_param(momentum=bn_param[0], eps=bn_param[1])

    def forward(self, x):
        x = self.first_conv(x)
        x = self.blocks(x)
        x = self.feature_mix_layer(x)
        x = self.global_avg_pooling(x)
        x = self.classifier(x)
        return x

    def set_bn_param(self, momentum, eps):
        for m in self.modules():
            if isinstance(m, nn.BatchNorm2d) or isinstance(m, nn.BatchNorm1d):
                m.momentum = momentum
                m.eps = eps
        return

    def init_model(self, model_init='he_fout', init_div_groups=False):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                if model_init == 'he_fout':
                    n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                    if init_div_groups:
                        n /= m.groups
                    m.weight.data.normal_(0, math.sqrt(2. / n))
                elif model_init == 'he_fin':
                    n = m.kernel_size[0] * m.kernel_size[1] * m.in_channels
                    if init_div_groups:
                        n /= m.groups
                    m.weight.data.normal_(0, math.sqrt(2. / n))
                else:
                    raise NotImplementedError
            elif isinstance(m, nn.BatchNorm2d) or isinstance(m, nn.BatchNorm1d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m, nn.Linear):
                stdv = 1. / math.sqrt(m.weight.size(1))
                m.weight.data.uniform_(-stdv, stdv)
                if m.bias is not None:
                    m.bias.data.zero_()

    @property
    def arch(self):
        arch = ''
        for module in self.blocks:
            if isinstance(module, MobileInvertedResidualBlock):
                index = module.mobile_inverted_conv.mask.cpu().detach().numpy().argmax()
                arch +=f'{index}-'
        return arch


if __name__ == '__main__':
    from hyperbox.mutator import RandomMutator
    net = MobileNet()
    rm = RandomMutator(net)
    x = torch.randn(2, 3, 64, 64)
    for i in range(10):
        rm.reset()
        y = net(x)
        print(net.arch)
