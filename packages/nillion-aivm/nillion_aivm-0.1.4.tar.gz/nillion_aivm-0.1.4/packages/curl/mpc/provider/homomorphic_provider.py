#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from .provider import TupleProvider


class HomomorphicProvider(TupleProvider):
    NAME = "HE"

    def generate_additive_triple(self, size0, size1, op, *args, **kwargs):
        """Generate multiplicative triples of given sizes"""
        raise NotImplementedError("HomomorphicProvider not implemented")

    def square(self, size):
        """Generate square double of given size"""
        raise NotImplementedError("HomomorphicProvider not implemented")

    def generate_xor_triple(self, size0, size1):
        """Generate xor triples of given size"""
        raise NotImplementedError("HomomorphicProvider not implemented")

    def wrap_rng(self, size, num_parties):
        """Generate random shared tensor of given size and sharing of its wraps"""
        raise NotImplementedError("HomomorphicProvider not implemented")

    def B2A_rng(self, size):
        """Generate random bit tensor as arithmetic and binary shared tensors"""
        raise NotImplementedError("HomomorphicProvider not implemented")

    def generate_one_hot(self, tensor_size, lut_size, device=None):
        """Generate lookup table vectors of given sizes"""
        raise NotImplementedError("HomomorphicProvider not implemented")

    def egk_trunc_pr_rng(self, size, l, m, device=None):
        """Generate random values for the [EGK+20] probabilistic truncation protocol."""
        raise NotImplementedError("HomomorphicProvider not implemented")
