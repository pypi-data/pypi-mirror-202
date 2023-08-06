# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import pytest
import torch

from madgrad import MADGRAD

@pytest.fixture(autouse=True)
def set_torch_seed():
    torch.manual_seed(1)
    yield

def test_invalid_momentum():
    weight = torch.randn(10, 5).float().cuda().requires_grad_()
    bias = torch.randn(10).float().cuda().requires_grad_()
    with pytest.raises(ValueError):
        MADGRAD([weight, bias], lr=1e-2, momentum=1.0)


def test_invalid_lr():
    weight = torch.randn(10, 5).float().cuda().requires_grad_()
    bias = torch.randn(10).float().cuda().requires_grad_()
    with pytest.raises(ValueError):
        MADGRAD([weight, bias], lr=0)
    with pytest.raises(ValueError):
        MADGRAD([weight, bias], lr=-1e-2)


def test_invalid_weight_decay():
    weight = torch.randn(10, 5).float().cuda().requires_grad_()
    bias = torch.randn(10).float().cuda().requires_grad_()
    with pytest.raises(ValueError):
        MADGRAD([weight, bias], weight_decay=-1)




def test_invalid_eps():
    weight = torch.randn(10, 5).float().cuda().requires_grad_()
    bias = torch.randn(10).float().cuda().requires_grad_()
    with pytest.raises(ValueError):
        MADGRAD([weight, bias], eps=-1)


def step_test(optimizer, weight, bias, input):
    # to check if the optimizer can be printed as a string
    optimizer.__repr__()

    def fn():
        optimizer.zero_grad()
        y = weight.mv(input)
        if y.is_cuda and bias.is_cuda and y.get_device() != bias.get_device():
            y = y.cuda(bias.get_device())
        loss = (y + bias).pow(2).sum()
        loss.backward()
        return loss

    initial_value = fn().item()
    for _i in range(5):
        optimizer.step(fn)
    print(fn().item())
    assert fn().item() < initial_value


def make_full_precision_params():
    weight = torch.randn(2, 1).cuda().requires_grad_()
    bias = torch.randn(2).cuda().requires_grad_()
    input = torch.randn(1).cuda()

    return weight, bias, input

def test_step_full_precision_inferred():
    weight, bias, input = make_full_precision_params()
    optimizer = MADGRAD([weight, bias], lr=1e-3)

    step_test(optimizer, weight, bias, input)

def test_momentum_zero():
    weight, bias, input = make_full_precision_params()
    optimizer = MADGRAD([weight, bias], lr=1e-3, momentum=0)

    step_test(optimizer, weight, bias, input)

def test_sparse():
    weight = torch.randn(5, 1).cuda().requires_grad_()
    weight_sparse = weight.detach().clone().requires_grad_()
    optimizer_dense = MADGRAD([weight], lr=1e-3, momentum=0)
    optimizer_sparse = MADGRAD([weight_sparse], lr=1e-3, momentum=0)

    weight.grad = torch.rand_like(weight)
    weight.grad[0] = 0.0  # Add a zero
    weight_sparse.grad = weight.grad.to_sparse()

    optimizer_dense.step()
    optimizer_sparse.step()
    assert torch.allclose(weight, weight_sparse)

    weight.grad = torch.rand_like(weight)
    weight.grad[1] = 0.0  # Add a zero
    weight_sparse.grad = weight.grad.to_sparse()

    optimizer_dense.step()
    optimizer_sparse.step()
    assert torch.allclose(weight, weight_sparse)

    weight.grad = torch.rand_like(weight)
    weight.grad[0] = 0.0  # Add a zero
    weight_sparse.grad = weight.grad.to_sparse()

    optimizer_dense.step()
    optimizer_sparse.step()
    assert torch.allclose(weight, weight_sparse)
