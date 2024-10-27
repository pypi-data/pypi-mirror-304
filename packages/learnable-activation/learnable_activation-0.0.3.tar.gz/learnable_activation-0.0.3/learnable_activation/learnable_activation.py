import torch
import torch.nn as nn


class LearnableActivation(nn.Module):
    def __init__(self, num_features, width=10, density=1):
        super(LearnableActivation, self).__init__()
        self.num_features = num_features
        self.width = width
        self.density = density

        num_control_points = width * density + 1
        range_values = torch.linspace(-width / 2, width / 2, num_control_points)

        self.interp_tensor = nn.Parameter(range_values.repeat(num_features, 1))
        self.register_buffer("feature_idx", torch.arange(self.num_features).view(1, -1))
        self.location = self.width * self.density / 2
        self.max_index = self.width * self.density

    def forward(self, x):
        scaled_x = (x * self.density) + self.location

        lower_idx = torch.clamp(scaled_x.long(), min=0, max=self.max_index - 1)
        upper_idx = lower_idx + 1

        lower_value = self.interp_tensor[self.feature_idx, lower_idx]
        upper_value = self.interp_tensor[self.feature_idx, upper_idx]

        interpolation_weight = scaled_x - lower_idx.float()
        return torch.lerp(lower_value, upper_value, interpolation_weight)
