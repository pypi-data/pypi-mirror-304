import torch
import torch.nn as nn
from .learnable_activation import LearnableActivation


class TabularDenseNet(nn.Module):
    def __init__(self, input_size, output_size, num_layers=2, width=20, density=1):
        super(TabularDenseNet, self).__init__()

        self.layers = nn.ModuleList()
        self.activations = nn.ModuleList()

        for i in range(num_layers):
            self.activations.append(LearnableActivation(input_size, width, density))
            self.layers.append(nn.Linear(input_size, input_size, bias=False))

            with torch.no_grad():
                self.layers[-1].weight.copy_(torch.eye(input_size))

            input_size *= 2

        self.activation_second_last_layer = LearnableActivation(input_size, width, density)
        self.last_layer = nn.Linear(input_size, output_size, bias=False)

        with torch.no_grad():
            self.last_layer.weight.copy_(torch.zeros(output_size, input_size))

        self.activation_last_layer = LearnableActivation(output_size, width, density)

    def forward(self, x):
        outputs = [x]

        for i in range(len(self.layers)):
            concatenated_outputs = torch.cat(outputs, dim=1)
            outputs.append(self.layers[i](self.activations[i](concatenated_outputs)))

        outputs = torch.cat(outputs, dim=1)
        outputs = self.activation_second_last_layer(outputs)
        outputs = self.last_layer(outputs)
        outputs = self.activation_last_layer(outputs)
        return outputs.squeeze()
