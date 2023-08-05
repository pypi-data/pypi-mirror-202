import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


__all__ = ["transI_fusebn", "transII_addbranch", "transIII_1x1_kxk",
           "transIV_depthconcat", "transV_avg", "transVI_multiscale", "DBBORIGIN", "DBB1x1", "DBBAVG", "DBB1x1kxk"]

#######################
# auxiliary operation #
#######################


class IdentityBasedConv1x1(nn.Conv2d):
    def __init__(self, channels, groups=1):
        super(IdentityBasedConv1x1, self).__init__(in_channels=channels,
                                                   out_channels=channels, kernel_size=1, stride=1, padding=0, groups=groups, bias=False)

        assert channels % groups == 0
        input_dim = channels // groups
        id_value = np.zeros((channels, input_dim, 1, 1))
        for i in range(channels):
            id_value[i, i % input_dim, 0, 0] = 1
        self.id_tensor = torch.from_numpy(id_value).type_as(self.weight)
        nn.init.zeros_(self.weight)

    def forward(self, input):
        kernel = self.weight + self.id_tensor.to(self.weight.device)
        result = F.conv2d(input, kernel, None, stride=1, padding=1,  # from 0 to 1
                          dilation=self.dilation, groups=self.groups)
        return result

    def get_actual_kernel(self):
        return self.weight + self.id_tensor.to(self.weight.device)


class BNAndPadLayer(nn.Module):
    def __init__(self,
                 pad_pixels,
                 num_features,
                 eps=1e-5,
                 momentum=0.1,
                 affine=True,
                 track_running_stats=True):
        super(BNAndPadLayer, self).__init__()
        self.bn = nn.BatchNorm2d(
            num_features, eps, momentum, affine, track_running_stats)
        self.pad_pixels = pad_pixels

    def forward(self, input):
        output = self.bn(input)
        if self.pad_pixels > 0:
            if self.bn.affine:
                pad_values = self.bn.bias.detach() - self.bn.running_mean * self.bn.weight.detach() / \
                    torch.sqrt(self.bn.running_var + self.bn.eps)
            else:
                pad_values = - self.bn.running_mean / \
                    torch.sqrt(self.bn.running_var + self.bn.eps)
            output = F.pad(output, [self.pad_pixels] * 4)
            pad_values = pad_values.view(1, -1, 1, 1)
            output[:, :, 0:self.pad_pixels, :] = pad_values
            output[:, :, -self.pad_pixels:, :] = pad_values
            output[:, :, :, 0:self.pad_pixels] = pad_values
            output[:, :, :, -self.pad_pixels:] = pad_values
        return output

    @property
    def weight(self):
        return self.bn.weight

    @property
    def bias(self):
        return self.bn.bias

    @property
    def running_mean(self):
        return self.bn.running_mean

    @property
    def running_var(self):
        return self.bn.running_var

    @property
    def eps(self):
        return self.bn.eps

############################
# Four Candidate Operation #
############################


class DBBORIGIN(nn.Module):
    # candidate operation 1
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1):
        super(DBBORIGIN, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.groups = groups
        self.padding = kernel_size // 2
        self.conv = nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size,
                              stride=stride, padding=self.padding, dilation=dilation, groups=groups, bias=False, padding_mode='zeros')
        self.bn = nn.BatchNorm2d(out_channels, affine=True)

    def forward(self, input):
        out = self.conv(input)
        out = self.bn(out)
        return out


class DBB1x1(nn.Module):
    # candidate operation 2
    def __init__(self, in_channels, out_channels, stride=1, padding=0, groups=1):
        super(DBB1x1, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = 1
        self.stride = stride
        self.padding = 0
        self.groups = groups
        self.conv = nn.Conv2d(in_channels=in_channels, out_channels=out_channels,
                              kernel_size=1, stride=stride, padding=0, groups=groups)
        self.bn = nn.BatchNorm2d(out_channels, affine=True)

    def forward(self, input):
        return self.bn(self.conv(input))


class DBBAVG(nn.Module):
    # candidate operation 3
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1):
        super(DBBAVG, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.groups = groups
        self.padding = kernel_size // 2
        self.dbb_avg = nn.Sequential()
        if groups < out_channels:
            self.dbb_avg.add_module('conv',
                                    nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=1,
                                              stride=1, padding=0, groups=groups, bias=False))
            self.dbb_avg.add_module('bn', BNAndPadLayer(
                pad_pixels=padding, num_features=out_channels))
            self.dbb_avg.add_module('avg', nn.AvgPool2d(
                kernel_size=kernel_size, stride=stride, padding=self.padding))
        else:
            self.dbb_avg.add_module('avg', nn.AvgPool2d(
                kernel_size=kernel_size, stride=stride, padding=self.padding))

        self.dbb_avg.add_module('avgbn', nn.BatchNorm2d(out_channels))

    def forward(self, input):
        return self.dbb_avg(input)


class DBB1x1kxk(nn.Module):
    # candidate operation 4
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, internal_channels_1x1_3x3=None):
        super(DBB1x1kxk, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.groups = groups
        self.padding = kernel_size // 2 
        if internal_channels_1x1_3x3 is None:
            internal_channels_1x1_3x3 = in_channels if groups < out_channels else 2 * \
                in_channels   # For mobilenet, it is better to have 2X internal channels
        self.dbb_1x1_kxk = nn.Sequential()

        if internal_channels_1x1_3x3 == in_channels:
            self.dbb_1x1_kxk.add_module('idconv1', IdentityBasedConv1x1(
                channels=in_channels, groups=groups))
        else:
            self.dbb_1x1_kxk.add_module('conv1', nn.Conv2d(in_channels=in_channels, out_channels=internal_channels_1x1_3x3,
                                                           kernel_size=1, stride=1, padding=0, groups=groups, bias=False))
        self.dbb_1x1_kxk.add_module('bn1', BNAndPadLayer(
            pad_pixels=padding, num_features=internal_channels_1x1_3x3, affine=True))
        padding = self.padding - 1
        self.dbb_1x1_kxk.add_module('conv2', nn.Conv2d(in_channels=internal_channels_1x1_3x3, out_channels=out_channels,
                                                       kernel_size=kernel_size, stride=stride, padding=padding, groups=groups, bias=False))
        self.dbb_1x1_kxk.add_module('bn2', nn.BatchNorm2d(out_channels))

    def forward(self, input):  # input: [5, 16, 32, 32]
        return self.dbb_1x1_kxk(input)

###############
# Fuse Kernel #
###############


def transI_fusebn(kernel, bn):
    gamma = bn.weight
    std = (bn.running_var + bn.eps).sqrt()
    return kernel * ((gamma / std).reshape(-1, 1, 1, 1)), bn.bias - bn.running_mean * gamma / std


def transII_addbranch(kernels, biases):
    return sum(kernels), sum(biases)


def transIII_1x1_kxk(k1, b1, k2, b2, groups):
    if groups == 1:
        k = F.conv2d(k2, k1.permute(1, 0, 2, 3))
        b_hat = (k2 * b1.reshape(1, -1, 1, 1)).sum((1, 2, 3))
    else:
        k_slices = []
        b_slices = []
        k1_T = k1.permute(1, 0, 2, 3)
        k1_group_width = k1.size(0) // groups
        k2_group_width = k2.size(0) // groups
        for g in range(groups):
            k1_T_slice = k1_T[:, g * k1_group_width:(g + 1) * k1_group_width, :, :]
            k2_slice = k2[g * k2_group_width:(g + 1) * k2_group_width, :, :, :]
            k_slices.append(F.conv2d(k2_slice, k1_T_slice))
            b_slices.append(
                (k2_slice * b1[g * k1_group_width:(g + 1) * k1_group_width].reshape(1, -1, 1, 1)).sum((1, 2, 3)))
        k, b_hat = transIV_depthconcat(k_slices, b_slices)
    return k, b_hat + b2


def transIV_depthconcat(kernels, biases):
    return torch.cat(kernels, dim=0), torch.cat(biases)


def transV_avg(channels, kernel_size, groups):
    input_dim = channels // groups
    k = torch.zeros((channels, input_dim, kernel_size, kernel_size))
    k[np.arange(channels), np.tile(np.arange(input_dim), groups), :, :] = 1.0 / kernel_size ** 2
    return k

#   This has not been tested with non-square kernels (kernel.size(2) != kernel.size(3)) nor even-size kernels


def transVI_multiscale(kernel, target_kernel_size):
    H_pixels_to_pad = (target_kernel_size - kernel.size(2)) // 2
    W_pixels_to_pad = (target_kernel_size - kernel.size(3)) // 2
    return F.pad(kernel, [H_pixels_to_pad, H_pixels_to_pad, W_pixels_to_pad, W_pixels_to_pad])


if __name__ == "__main__":
    m = DBB1x1kxk(3, 6, 3)
    input = torch.zeros(5, 3, 32, 32)
    print(m(input).shape)
