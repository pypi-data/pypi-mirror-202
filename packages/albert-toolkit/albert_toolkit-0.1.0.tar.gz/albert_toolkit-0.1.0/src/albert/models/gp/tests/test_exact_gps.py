import pytest

import numpy as np
import gpytorch
import torch
from albert.models.gp import NDExactGPModel
from typing import Type


@pytest.fixture
def model_opts():
    return {"kernel_type": "rbf"}


@pytest.fixture
def simple_input():
    xdata = torch.Tensor(np.linspace(-5, 5, 20))
    ydata = torch.Tensor(np.sin(xdata))

    return {"x": xdata.unsqueeze(0), "y": ydata.unsqueeze(0)}


def contains_module_of_type(parent: torch.nn.Module, instance_type: Type):
    for cc in parent.modules():
        if isinstance(cc, instance_type):
            return True
    return False


# No model opts should lead to a default kernel configuration
def test_ndegp_no_model_options():
    model = NDExactGPModel([], [], gpytorch.likelihoods.GaussianLikelihood(), None)
    assert contains_module_of_type(model, gpytorch.kernels.RBFKernel)
    assert contains_module_of_type(model, gpytorch.kernels.LinearKernel)


@pytest.mark.xfail
def test_ndegp_missing_nu_value(simple_input, model_opts):
    """
    This test is to make sure that if the model_opts dictionary doesn't contain a nu
    element that the system provides the correct behavior -- which I am not sure what
    that is
    """
    # set the kernel type to matern but do not set a 'nu' value
    model_opts["kernel_type"] = "matern"

    # What is our expected behavior here? -- will we assign a default value internally or
    # should we error out?
    model = NDExactGPModel(
        simple_input["x"],
        simple_input["y"],
        gpytorch.likelihoods.GaussianLikelihood(),
        model_opts,
    )

    # based on the current code we would expect that perhaps
    # the nu value should be set to 3.5 and we should have the
    # matern kernel
    assert contains_module_of_type(
        model, gpytorch.kernels.MaternKernel
    ), "module doesn't contain the matern kernel, but should"

    for cc in model.modules():
        if isinstance(cc, gpytorch.kernels.MaternKernel):
            assert cc.nu is not None
            assert cc.nu == 3.5

@pytest.mark.xfail
def test_ndegp_bad_kernel_type(simple_input, model_opts):

    model_opts["kernel_type"] = "notakernel"

    # If we do not specify a valid kernel this should raise
    # an exception to alert the user that this won't work
    with pytest.raises(ValueError):
        _ = NDExactGPModel(
            simple_input["x"],
            simple_input["y"],
            gpytorch.likelihoods.GaussianLikelihood(),
            model_opts,
        )


def test_ndegp_valid_params(simple_input, model_opts):
    model = NDExactGPModel(
        simple_input["x"],
        simple_input["y"],
        gpytorch.likelihoods.GaussianLikelihood(),
        model_opts,
    )
    assert contains_module_of_type(
        model, gpytorch.kernels.RBFKernel
    ), "the GP should have an RBF kernel"
    
    assert not contains_module_of_type(
        model, gpytorch.kernels.LinearKernel
    ), "the GP should not have had a linear kernel"
