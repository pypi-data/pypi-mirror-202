import pytest
import torch

from albert.models.nn.embedding import MLPEmbedding


def test_mlp_bad_n_hidden():
    """
    Tests to make sure that if the user passes in a negative number for the num
    of hidden layers that an exception is raised
    """
    with pytest.raises(
        ValueError,
        match="n_hidden < 0 -- you must specify a number greater than or equal to zero for the"
        " number of hidden layers",
    ):
        _ = MLPEmbedding(100, 100, -1, 100)


def test_mlp_bad_dims():
    """
    Test to ensure that if an MLP is passed in a parameter value which is not valid it will
    raise a nice error rather than some internal pytorch error
    """
    with pytest.raises(ValueError, match=r"the dimensions must all be >= 1 .*"):
        _ = MLPEmbedding(0, 100, 10, 100)

    with pytest.raises(ValueError, match=r"the dimensions must all be >= 1 .*"):
        _ = MLPEmbedding(10, 0, 10, 100)

    with pytest.raises(ValueError, match=r"the dimensions must all be >= 1 .*"):
        _ = MLPEmbedding(10, 100, 10, 0)


def test_mlp_create():
    """
    Test to ensure no exceptions are rasied when valid parameters are used to create an MLP
    network
    """
    _ = MLPEmbedding(10, 125, 2, 8)
    _ = MLPEmbedding(1, 3, 5, 7)
    _ = MLPEmbedding(7, 5, 3, 1)


@pytest.mark.usefixtures("seeded")
def test_mlp_architecture_with_hidden():
    """
    Tests to ensure that the output tensor shape matches what is expected given
    the input parameters -- runs 25 different builds with different architecture parameters
    """

    for i in range(25):
        indim = torch.randint(1, 250, size=(1,)).item()
        outdim = torch.randint(1, 250, size=(1,)).item()
        hdim = torch.randint(1, 250, size=(1,)).item()
        nhidden = torch.randint(1, 25, size=(1,)).item()
        net = MLPEmbedding(indim, hdim, nhidden, outdim)
        out = net.forward(torch.randn((13, indim)))
        assert out.shape == torch.Size((13, outdim))


@pytest.mark.usefixtures("seeded")
def test_mlp_architecture_without_hidden():
    """
    Tests to ensure that if the user passes in 0 for n_hidden that the MLP produces the
    correct output shape
    """

    net = MLPEmbedding(10, 13, 0, 25)
    out = net.forward(torch.randn((15, 10)))
    assert out.shape == torch.Size((15, 25))


@pytest.mark.usefixtures("seeded")
def test_mlp_normalized_output():
    """
    Tests to ensure that when the normalize flag in the MLPEmbedding init function is set,
    the resulting tensor returned is normalized along the embedding dimension.
    """
    torch.manual_seed(42)
    net = MLPEmbedding(10, 10, 10, 10, normalize=False)
    norm = torch.linalg.norm(net.forward(torch.randn((13, 10))))
    assert torch.max(norm - torch.ones((13,))) > 1e-5

    net = MLPEmbedding(10, 10, 10, 10, normalize=True)
    output = net.forward(torch.randn((13, 10)))
    norm = torch.linalg.norm(output, 2, dim=-1)
    assert torch.max(norm - torch.ones((13,))) < 1e-5


def test_mlp_bad_activation_name():
    """
    Tests to ensure that the MLPEmbedding class raises an exception when an
    unknown activation layer type is specified
    """

    # bloop is not a valid activation layer type -- so this should raise a
    # ValueError indicating that the type was not known
    with pytest.raises(ValueError, match=r"unknown activation layer bloop"):
        _ = MLPEmbedding(10, 10, 10, 10, activation="bloop")

    # We will also check that valid sets
    _ = MLPEmbedding(10, 10, 10, 10, "celu")
    _ = MLPEmbedding(10, 10, 10, 10, "relu")
