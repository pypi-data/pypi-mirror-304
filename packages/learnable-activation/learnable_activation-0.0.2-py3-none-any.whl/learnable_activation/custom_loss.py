from torch import nn
from .learnable_activation import LearnableActivation


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
