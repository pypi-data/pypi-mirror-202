# import math
# import warnings
# from collections import OrderedDict
# from typing import Any, Callable, Dict, List, Optional, Tuple

# import torch
from torch import Tensor, nn
from torch.nn.functional import normalize


def _act(name: str) -> nn.Module:
    if name == "relu":
        return nn.ReLU()
    elif name == "celu":
        return nn.CELU()
    else:
        raise ValueError(f"unknown activation layer {name}")


class MLPEmbedding(nn.Module):
    """
    A simple MLP Network Architecture that embeds into a latent space.

    A typical use case for this network is as a latent distentangling network, however it can be
    used as simple way to generate embeddings from any flattened input

    Args:
        in_dim      (int): the dimension of the input tensor
        hidden_dim  (int): the dimension iof the hidden layers
        n_hidden    (int): number of hidden layers in the MLP
        output_dim  (int): the dimension of the output latent vector
        activation  (str): activation function to use - defaults to 'relu'
        normalize   (bool): whether or not to normalize the output of the network
                             -- defaults to True
    """

    def __init__(
        self,
        in_dim: int,
        hidden_dim: int,
        n_hidden: int,
        output_dim: int,
        activation: str = "relu",
        normalize: bool = True,
    ) -> None:
        super().__init__()

        self.normalize = normalize
        self.stack = nn.Sequential()

        if n_hidden < 0:
            raise ValueError(
                "n_hidden < 0 -- you must specify a number greater than or equal to zero for the"
                " number of hidden layers"
            )

        if in_dim < 1 or hidden_dim < 1 or output_dim < 1:
            raise ValueError(
                f"the dimensions must all be >= 1 got {in_dim}|{hidden_dim}|{output_dim} "
                "for input, hidden, and output respectively"
            )

        if n_hidden == 0:
            # If the user has not specified that we have hidden dimensions then we will
            # simply have a basic linear transform (no activations)
            self.stack.append(nn.Linear(in_dim, output_dim))
        else:
            # Create the Head of the MLP Stack
            self.stack.append(nn.Linear(in_dim, hidden_dim))
            self.stack.append(_act(activation))

            # Construct the stack of hidden layers
            for i in range(n_hidden - 1):
                self.stack.append(nn.Linear(hidden_dim, hidden_dim))
                self.stack.append(_act(activation))

            # Add on the final output layer to embed into the latent space
            self.stack.append(nn.Linear(hidden_dim, output_dim))

    def forward(self, x: Tensor) -> Tensor:
        if self.normalize:
            return normalize(self.stack.forward(x), 2, -1)
        else:
            return self.stack.forward(x)
