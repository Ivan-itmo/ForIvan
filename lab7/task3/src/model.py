from __future__ import annotations

import torch
from torch import nn


class CovidRiskNet(nn.Module):
    """Небольшой MLP для табличной бинарной классификации."""

    def __init__(
        self,
        input_size: int,
        hidden_size: int = 32,
        second_hidden_size: int = 16,
        dropout: float = 0.35,
        second_dropout: bool = True,
    ):
        super().__init__()
        if hidden_size <= 0 or second_hidden_size <= 0:
            raise ValueError("Размеры скрытых слоёв должны быть положительными")
        if not 0 <= dropout < 1:
            raise ValueError("dropout должен быть в диапазоне [0, 1)")

        layers: list[nn.Module] = [
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size, second_hidden_size),
            nn.ReLU(),
        ]
        if second_dropout:
            layers.append(nn.Dropout(dropout))
        layers.append(nn.Linear(second_hidden_size, 1))

        self.layers = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layers(x).squeeze(1)
