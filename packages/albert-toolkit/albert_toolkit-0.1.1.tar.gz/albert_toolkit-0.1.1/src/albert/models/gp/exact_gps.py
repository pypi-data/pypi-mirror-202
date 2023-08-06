import gpytorch.distributions as distributions
import gpytorch.kernels as kernels
import gpytorch.means as means

# import numpy as np
# import pandas as pd
# import torch
from gpytorch.models.exact_gp import ExactGP

# from sklearn import preprocessing
# from sklearn.model_selection import train_test_split


class NDExactGPModel(ExactGP):
    def __init__(self, train_x, train_y, likelihood, model_options=None):
        super(NDExactGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = means.ZeroMean()
        try:
            if model_options["kernel_type"].lower() == "rbf":
                self.covar_module = kernels.ScaleKernel(
                    kernels.RBFKernel(ard_num_dims=train_x.shape[1])
                )
            elif model_options["kernel_type"].lower() == "matern":
                nu = model_options["nu"] if model_options["nu"] is not None else 3.5
                self.covar_module = kernels.ScaleKernel(
                    kernels.MaternKernel(nu=nu, ard_num_dims=train_x.shape[1])
                    + kernels.LinearKernel()
                )
            else:
                raise Exception("RBF or Matern kernel must be used.")

                # self.covar_module = gpytorch.kernels.ScaleKernel(gpytorch.kernels.MaternKernel(nu=3.5,
                # ard_num_dims=train_x.shape[1]))
        except Exception:
            self.covar_module = kernels.ScaleKernel(
                kernels.RBFKernel() + kernels.LinearKernel()
            )

    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return distributions.MultivariateNormal(mean_x, covar_x)
