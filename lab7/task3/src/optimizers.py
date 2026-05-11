from __future__ import annotations

from typing import Iterable

import torch
from torch.optim import Optimizer


class MyRMSprop(Optimizer):
    """
    Собственная реализация RMSProp для PyTorch.

    Формула такая же, как в задании 2:
        G = gamma * G + (1 - gamma) * grad^2
        w = w - lr * grad / (sqrt(G) + eps)
    """

    def __init__(
        self,
        params: Iterable[torch.nn.Parameter],
        lr: float = 0.001,
        alpha: float = 0.99,
        eps: float = 1e-8,
        weight_decay: float = 0.0,
    ):
        if lr <= 0:
            raise ValueError("lr должен быть положительным")
        if not 0 <= alpha < 1:
            raise ValueError("alpha должен быть в диапазоне [0, 1)")
        if eps <= 0:
            raise ValueError("eps должен быть положительным")
        if weight_decay < 0:
            raise ValueError("weight_decay не может быть отрицательным")

        defaults = {"lr": lr, "alpha": alpha, "eps": eps, "weight_decay": weight_decay}
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        for group in self.param_groups:
            lr = group["lr"]
            alpha = group["alpha"]
            eps = group["eps"]
            weight_decay = group["weight_decay"]

            for parameter in group["params"]:
                if parameter.grad is None:
                    continue

                grad = parameter.grad
                if weight_decay != 0:
                    grad = grad.add(parameter, alpha=weight_decay)
                state = self.state[parameter]

                if len(state) == 0:
                    state["square_avg"] = torch.zeros_like(parameter)

                square_avg = state["square_avg"]
                square_avg.mul_(alpha).addcmul_(grad, grad, value=1.0 - alpha)

                denominator = square_avg.sqrt().add_(eps)
                parameter.addcdiv_(grad, denominator, value=-lr)

        return loss
