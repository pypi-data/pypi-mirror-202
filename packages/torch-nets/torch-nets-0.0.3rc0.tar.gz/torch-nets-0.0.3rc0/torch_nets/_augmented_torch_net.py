
__module_name__ = "__init__.py"
__doc__ = """
          Module contianing the API for accessing AugmentedTorchNets. This module
          remains under active development and testing.
          """
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])


# -- import packages: ----------------------------------------------------------
import torch
from typing import Union
import ABCParse


# -- import local dependencies: ------------------------------------------------
from ._torch_net import TorchNet


# -- primary module: -----------------------------------------------------------
class AugmentedTorchNet(torch.nn.Module, ABCParse.ABCParse):
    """
    TorchNet with additional torch.nn.Linear layer.
    Transforms (in_dim + n_aug) -> out_dim.

    Source:
    -------
     - paper:  https://arxiv.org/abs/1904.01681
     - GitHub: https://github.com/EmilienDupont/augmented-neural-odes
    """
    def __init__(
        self,
        in_features: int,
        out_features: int,
        hidden: Union[list, int] = [],
        activation=["LeakyReLU"],
        dropout: Union[float, list] = [0.2],
        bias: bool = [True],
        n_augment: int = 0,
        output_bias: bool = True,
    ):
        """
        Augmented TorchNet.

        Parameters:
        -----------
        in_features
            type: int
        
        out_features
            type: int
        
        hidden
            Hidden layer structure (e.g., [400, 400])
            type: List[int]
        
        activation
            Specifices activation function
            type: Any
        
        dropout
            type: List[float]
            default: [0.2]
        
        bias
            type: List[bool]
            default: [True]
            
        n_augment
            Number of augmented dimensions.
            type: int
        
        output_bias
            type: bool
            default: False
        

        Returns:
        --------
        None, instantiates torch.nn.Module for augmented neural network.

        Examples:
        ---------
        
        Notes:
        ------
        -> updates self.in_features
        -> updates self.out_features
        
        """
        
        super(AugmentedTorchNet, self).__init__()

        self._in_features_orig = in_features
        self._out_features_orig = out_features
        in_features += n_augment
        out_features += n_augment

        self.net = TorchNet(
            **ABCParse.function_kwargs(TorchNet, kwargs=locals())
        )

        self.__parse__(locals(), ignore=["net"])

        if n_augment > 0:
            self._configure_augmented_output()

    def _configure_augmented_output(self):
        self.net.names.append("augmented_output")
        self.net.extend([torch.nn.Linear(self.out_features, self._out_features_orig)])
        self.net._rename_nn_sequential_inplace(self.net, self.net.names)

    def augment_input(self, input):
        x_aug = torch.zeros(input.shape[0], self.n_augment, device=input.device)
        return torch.cat([input, x_aug], 1)

    def forward(self, input):
        return self.net(self.augment_input(input))

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(in_features={self._in_features_orig}, "
            f"out_features={self._out_features_orig}, net={repr(self.net)})"
        )
