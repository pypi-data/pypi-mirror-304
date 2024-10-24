#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import math

import numpy as np
import torch

DEFAULT_PRECISION_BITS = 16


# helper functions that determine if input is float, int, or base tensor:
def _is_type_tensor(tensor, types):
    """Checks whether the elements of the input tensor are of a given type"""
    if is_tensor(tensor):
        if any(tensor.dtype == type_ for type_ in types):
            return True
    return False


def is_tensor(tensor):
    """Checks if the input tensor is a Torch tensor or a CUDALongTensor"""
    return torch.is_tensor(tensor)


def is_float_tensor(tensor):
    """Checks if the input tensor is a Torch tensor of a float type."""
    return _is_type_tensor(tensor, [torch.float16, torch.float32, torch.float64])


def is_int_tensor(tensor):
    """Checks if the input tensor is a Torch tensor of an int type."""
    return _is_type_tensor(
        tensor, [torch.uint8, torch.int8, torch.int16, torch.int32, torch.int64]
    )


def nearest_integer_division(tensor, integer):
    """Performs division of integer tensor, rounding to nearest integer."""
    assert integer > 0, "only supports positive divisors"
    assert is_int_tensor(tensor), "unsupported type: %s" % type(tensor)

    lez = (tensor < 0).long()
    pos_remainder = (1 - lez) * tensor % integer
    neg_remainder = lez * ((integer - tensor) % integer)
    remainder = pos_remainder + neg_remainder
    quotient = tensor.div(integer, rounding_mode="trunc")
    correction = (2 * remainder > integer).long()
    return quotient + tensor.sign() * correction


class FixedPointEncoder:
    """Encoder that encodes long or float tensors into scaled integer tensors."""

    def __init__(self, precision_bits=None):
        if precision_bits is None:
            precision_bits = DEFAULT_PRECISION_BITS
        self._precision_bits = precision_bits
        self._scale = int(2**precision_bits)

    def encode(self, x, device=None):
        """Helper function to wrap data if needed"""
        if isinstance(x, int) or isinstance(x, float):
            # Squeeze in order to get a 0-dim tensor with value `x`
            return torch.tensor(
                [self._scale * x], dtype=torch.long, device=device
            ).squeeze()
        elif isinstance(x, list):
            return (
                torch.tensor(x, dtype=torch.float, device=device)
                .mul_(self._scale)
                .long()
            )
        elif is_float_tensor(x):
            return (self._scale * x).long()
        # For integer types cast to long prior to scaling to avoid overflow.
        elif is_int_tensor(x):
            return self._scale * x.long()
        elif isinstance(x, np.ndarray):
            return self._scale * torch.from_numpy(x).long().to(device)
        elif torch.is_tensor(x):
            raise TypeError("Cannot encode input with dtype %s" % x.dtype)
        else:
            raise TypeError("Unknown tensor type: %s." % type(x))

    def decode(self, tensor):
        """Helper function that decodes from scaled tensor"""
        if tensor is None:
            return None
        assert is_int_tensor(tensor), "input must be a LongTensor"
        if self._scale > 1:
            correction = (tensor < 0).long()
            dividend = tensor.div(self._scale - correction, rounding_mode="floor")
            remainder = tensor % self._scale
            remainder += (remainder == 0).long() * self._scale * correction

            tensor = dividend.float() + remainder.float() / self._scale
        else:
            tensor = nearest_integer_division(tensor, self._scale)

        return tensor.data

    def __setattr__(self, name, value):
        if name == "_precision_bits":
            dict.__setattr__(self, "_scale", int(2**value))
        elif name == "_scale":
            dict.__setattr__(self, "_precision_bits", int(math.log2(value)))
        dict.__setattr__(self, name, value)

    @property
    def scale(self):
        return self._scale

    @property
    def precision_bits(self):
        return self._precision_bits
