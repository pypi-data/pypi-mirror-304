### Quick Start
Three classes are available: LearnableActivation, TabularDenseNet, and CustomLoss.

LearnableActivation is, as the name suggests, a learnable activation function, which take in n inputs and create n outputs. It is first initialized as a linear activation function, where the shape is learned through placing various points across a predefined width, and interpolated over those points. Points outside of predefined width will be extrapolated.

Example LearnableActivation initialization:
```python
from learnable_activation import LearnableActivation
activation = LearnableActivation(input_size, width, density)
```

The width parameter is default initialized as 20 which interpolates over the range -10 and 10, and extrapolate outside that range. The density parameter determine how many data points will be packed in an interval with width of 1. Default density is 1.

### Class Definitions
```python
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
```

```python
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
```

```python
class CustomLoss(nn.Module):
    def __init__(self, criterion, l1_lambda=0.0, l2_lambda=0.0, f1_lambda=0.0, f2_lambda=0.0):
        super(CustomLoss, self).__init__()
        self.criterion = criterion
        self.l1_lambda = l1_lambda
        self.l2_lambda = l2_lambda
        self.f1_lambda = f1_lambda
        self.f2_lambda = f2_lambda

    def forward(self, outputs, labels, model):
        l1_norm = sum(
            p.abs().sum()
            for name, module in model.named_modules()
            if isinstance(module, nn.Linear)
            for p in module.parameters()
            if "bias" not in name
        )
        l1_loss = self.l1_lambda * l1_norm

        l2_norm = sum(
            p.pow(2.0).sum()
            for name, module in model.named_modules()
            if isinstance(module, nn.Linear)
            for p in module.parameters()
            if "bias" not in name
        )
        l2_loss = self.l2_lambda * l2_norm

        f1_loss = 0
        f2_loss = 0
        for name, module in model.named_modules():
            if isinstance(module, LearnableActivation):
                copy_tensor = module.copy_tensor

                f1_diff = copy_tensor[:, 1:] - copy_tensor[:, :-1]
                f1_loss += self.f1_lambda * f1_diff.abs().sum()

                f2_diff = f1_diff[:, 1:] - f1_diff[:, :-1]
                f2_loss += self.f2_lambda * f2_diff.abs().sum()

        return self.criterion(outputs, labels) + l1_loss + l2_loss + f1_loss + f2_loss

    def regular_loss(self, outputs, labels):
        return self.criterion(outputs, labels)
```