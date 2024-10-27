import torch
import torch.nn as nn


class LearnableActivation(nn.Module):
    def __init__(self, num_features, width=20, density=1):
        super(LearnableActivation, self).__init__()
        self.num_features = num_features
        self.width = width
        self.density = density

        num_intervals = width * density
        range_values = torch.linspace(-width / 2, width / 2, num_intervals + 1)
        self.copy_tensor = nn.Parameter(range_values.repeat(num_features, 1))
        self.feature_idx = torch.arange(self.num_features).view(1, -1)

    def forward(self, x):
        scaled_x = (x * self.density) + (self.width * self.density / 2)

        lower_idx = torch.floor(scaled_x).long()
        lower_idx = torch.clamp(lower_idx, min=0, max=self.copy_tensor.size(1) - 2)
        upper_idx = lower_idx + 1

        lower_value = self.copy_tensor[self.feature_idx, lower_idx]
        upper_value = self.copy_tensor[self.feature_idx, upper_idx]

        interp_factor = scaled_x - lower_idx.float()
        interpolated_value = torch.lerp(lower_value, upper_value, interp_factor)
        return interpolated_value
