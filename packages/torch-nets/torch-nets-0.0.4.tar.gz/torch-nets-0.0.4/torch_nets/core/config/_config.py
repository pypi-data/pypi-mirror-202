
from ._layer_wise_attributes_config import LayerWiseAttributesConfig
from ._activation_function_config import ActivationFunctionConfig
from ._network_structure_config import NetworkStructureConfig


from ABCParse import ABCParse


# -- operator class: ------------------------------------------------------
class Config(ABCParse):
    def __init__(self, in_features, out_features, hidden):
        self.__parse__(locals())
        
        self._NETWORK_STRUCTURE = NetworkStructureConfig()
        self._ACTIVATION_FUNCTION = ActivationFunctionConfig()
        self._LAYERWISE_ATTRIBUTES = LayerWiseAttributesConfig(
            n_hidden=self.n_hidden
        )

    @property
    def n_hidden(self):
        return len(self.hidden)

    @property
    def activation_function(self):
        return self._ACTIVATION_FUNCTION

    @property
    def network_structure(self):
        return self._NETWORK_STRUCTURE(self.in_features, self.out_features, self.hidden)

    @property
    def layerwise_attributes(self):
        return self._LAYERWISE_ATTRIBUTES