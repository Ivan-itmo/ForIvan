from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MPL_DIR = ROOT / ".mpl-cache"
CACHE_DIR = ROOT / ".cache"
MPL_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_DIR.resolve()))
os.environ.setdefault("XDG_CACHE_HOME", str(CACHE_DIR.resolve()))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

try:
    import torch
except ImportError:
    torch = None


BOX = (-4.0, 4.0, -4.0, 4.0)
SADDLE = np.array([-1.0, 2.5], dtype=float)
GLOBAL_MIN = np.array([-3.0 / 16.0, -4.0], dtype=float)
POS_EIGENVECTOR = np.array([-0.99250756, -0.12218326], dtype=float)
NEG_EIGENVECTOR = np.array([0.12218326, -0.99250756], dtype=float)
START = SADDLE + 3.0 * POS_EIGENVECTOR + 1e-3 * NEG_EIGENVECTOR


@dataclass
class RunResult:
    history: np.ndarray
    iterations: int
    final_point: np.ndarray
    final_value: float


def f(point: np.ndarray) -> float:
    x, y = point
    return 1e-2 * (8 * x * x + 2 * x * y + 11 * x + 2 * y + 3)


def grad(point: np.ndarray) -> np.ndarray:
    x, y = point
    return 1e-2 * np.array([16 * x + 2 * y + 11, 2 * x + 2], dtype=float)


def project(point: np.ndarray) -> np.ndarray:
    xmin, xmax, ymin, ymax = BOX
    return np.array(
        [np.clip(point[0], xmin, xmax), np.clip(point[1], ymin, ymax)],
        dtype=float,
    )


def gradient_descent(
    start: np.ndarray,
    lr: float,
    max_iters: int = 97,
    grad_tol: float | None = None,
    func_tol: float | None = None,
) -> RunResult:
    x = start.astype(float).copy()
    history = [x.copy()]
    prev_value = f(x)

    for iteration in range(1, max_iters + 1):
        x = x - lr * grad(x)
        history.append(x.copy())
        current_value = f(x)
        if grad_tol is not None and func_tol is not None:
            if np.linalg.norm(grad(x)) < grad_tol and abs(current_value - prev_value) < func_tol:
                return RunResult(np.array(history), iteration, x, current_value)
        prev_value = current_value

    return RunResult(np.array(history), max_iters, x, f(x))


def heavy_ball(
    start: np.ndarray,
    lr: float,
    gamma: float,
    max_iters: int,
) -> RunResult:
    x = start.astype(float).copy()
    avg_sq_grad = np.zeros_like(x)
    history = [x.copy()]

    for _ in range(max_iters):
        current_grad = grad(x)
        avg_sq_grad = gamma * avg_sq_grad + (1.0 - gamma) * (current_grad ** 2)
        x = project(x - lr * current_grad / (np.sqrt(avg_sq_grad) + 1e-8))
        history.append(x.copy())

    return RunResult(np.array(history), max_iters, x, f(x))


def torch_sgd_momentum(
    start: np.ndarray,
    lr: float,
    gamma: float,
    max_iters: int,
) -> RunResult:
    if torch is None:
        raise RuntimeError("PyTorch is not installed.")

    xmin, xmax, ymin, ymax = BOX
    point = torch.tensor(start, dtype=torch.float64, requires_grad=True)
    optimizer = torch.optim.RMSprop([point], lr=lr, alpha=gamma, eps=1e-8)
    history = [start.astype(float).copy()]

    for _ in range(max_iters):
        optimizer.zero_grad()
        x, y = point[0], point[1]
        value = 1e-2 * (8 * x * x + 2 * x * y + 11 * x + 2 * y + 3)
        value.backward()
        optimizer.step()
        with torch.no_grad():
            point[0].clamp_(xmin, xmax)
            point[1].clamp_(ymin, ymax)
        history.append(point.detach().cpu().numpy().copy())

    final_point = history[-1]
    return RunResult(np.array(history), max_iters, final_point, f(final_point))


def make_grid(
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    points: int = 500,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    xs = np.linspace(*xlim, points)
    ys = np.linspace(*ylim, points)
    xx, yy = np.meshgrid(xs, ys)
    zz = 1e-2 * (8 * xx * xx + 2 * xx * yy + 11 * xx + 2 * yy + 3)
    return xx, yy, zz


def plot_contours(
    output: Path,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    trajectories: list[tuple[str, np.ndarray, str]],
    title: str,
) -> None:
    xx, yy, zz = make_grid(xlim, ylim)
    plt.figure(figsize=(9, 7))
    contours = plt.contour(xx, yy, zz, levels=24, cmap="viridis")
    plt.clabel(contours, inline=True, fontsize=8)

    xmin, xmax, ymin, ymax = BOX
    plt.plot(
        [xmin, xmax, xmax, xmin, xmin],
        [ymin, ymin, ymax, ymax, ymin],
        color="black",
        linewidth=1.2,
        linestyle="--",
        label="граница области",
        zorder=2,
    )
    plt.scatter(*SADDLE, color="red", s=90, marker="x", label="седловая точка", zorder=5)
    plt.scatter(
        *GLOBAL_MIN,
        color="green",
        s=180,
        marker="*",
        edgecolors="black",
        linewidths=0.7,
        label="глобальный минимум",
        zorder=6,
    )
    plt.scatter(
        *START,
        color="orange",
        s=120,
        marker="o",
        edgecolors="black",
        linewidths=0.7,
        label="начальное приближение",
        zorder=6,
    )
    plt.annotate(
        "x0",
        xy=START,
        xytext=(8, 8),
        textcoords="offset points",
        fontsize=10,
        color="black",
    )
    plt.annotate(
        "xmin",
        xy=GLOBAL_MIN,
        xytext=(8, 10),
        textcoords="offset points",
        fontsize=10,
        color="black",
    )

    for label, history, color in trajectories:
        plt.plot(history[:, 0], history[:, 1], color=color, linewidth=2, label=label)
        step = max(1, len(history) // 20)
        plt.scatter(history[::step, 0], history[::step, 1], color=color, s=16)

    x_pad = 0.08 * (xlim[1] - xlim[0])
    y_pad = 0.08 * (ylim[1] - ylim[0])
    plt.xlim(xlim[0] - x_pad, xlim[1] + x_pad)
    plt.ylim(ylim[0] - y_pad, ylim[1] + y_pad)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output, dpi=180)
    plt.close()


def main() -> None:
    plots_dir = ROOT / "plots"
    plots_dir.mkdir(exist_ok=True)

    gd_result = gradient_descent(
        start=START,
        lr=0.7,
        max_iters=200,
        grad_tol=5e-6,
        func_tol=1e-9,
    )
    fixed_steps = gd_result.iterations
    gd_fixed = gradient_descent(start=START, lr=0.7, max_iters=fixed_steps)
    rms_escape = heavy_ball(start=START, lr=0.8, gamma=0.99, max_iters=fixed_steps)
    rms_zigzag = heavy_ball(start=START, lr=1.3, gamma=0.97, max_iters=fixed_steps)
    rms_direct = heavy_ball(start=START, lr=0.5, gamma=0.99, max_iters=fixed_steps)

    contour_xlim = (-4.0, 1.0)
    contour_ylim = (-4.0, 3.0)

    plot_contours(
        plots_dir / "gd_to_saddle.png",
        contour_xlim,
        contour_ylim,
        [("градиентный спуск", gd_fixed.history, "#d94841")],
        "Задание 2.1: градиентный спуск приближается к седловой точке",
    )
    plot_contours(
        plots_dir / "rmsprop_escape.png",
        contour_xlim,
        contour_ylim,
        [("градиентный спуск", gd_fixed.history, "#d94841"), ("RMSProp", rms_escape.history, "#2b8cbe")],
        "Задание 2.2: RMSProp преодолевает окрестность седловой точки",
    )
    plot_contours(
        plots_dir / "hyperparams_compare.png",
        contour_xlim,
        contour_ylim,
        [("пилообразно", rms_zigzag.history, "#f16913"), ("более прямо", rms_direct.history, "#238b45")],
        "Задание 2.3: одна область, разные гиперпараметры RMSProp",
    )

    print("Задание 2")
    print("==========")
    print("Пункт 1. Обычный градиентный спуск")
    print(f"Начальное приближение: x0 = ({START[0]:.8f}, {START[1]:.8f})")
    print("Скорость обучения: alpha = 0.7")
    print("Критерий останова:")
    print("||grad f(x_k)|| < 5e-6 и |f(x_k) - f(x_(k-1))| < 1e-9")
    print(f"Количество итераций: {fixed_steps}")
    print(f"Последняя точка: ({gd_result.final_point[0]:.8f}, {gd_result.final_point[1]:.8f})")
    print(f"Значение функции: {gd_result.final_value:.10f}")
    print()
    print("Пункт 2. Эвристика RMSProp")
    print("Параметры: alpha = 0.8, gamma = 0.99")
    print(f"Последняя точка: ({rms_escape.final_point[0]:.8f}, {rms_escape.final_point[1]:.8f})")
    print(f"Значение функции: {rms_escape.final_value:.10f}")
    print("За то же число итераций траектория выходит из окрестности седла")
    print("и приходит к глобальному минимуму на границе области.")
    print()
    print("Пункт 3. Подбор гиперпараметров при той же области отображения")
    print("Область отображения: x in [-4, 1], y in [-4, 3]")
    print("Пилообразная траектория: alpha = 1.3, gamma = 0.97")
    print(f"Последняя точка: ({rms_zigzag.final_point[0]:.8f}, {rms_zigzag.final_point[1]:.8f})")
    print("Более направленное движение: alpha = 0.5, gamma = 0.99")
    print(f"Последняя точка: ({rms_direct.final_point[0]:.8f}, {rms_direct.final_point[1]:.8f})")

    if torch is not None:
        torch_result = torch_sgd_momentum(START, lr=0.8, gamma=0.99, max_iters=fixed_steps)
        plot_contours(
            plots_dir / "torch_rmsprop.png",
            contour_xlim,
            contour_ylim,
            [("PyTorch RMSProp", torch_result.history, "#6a51a3")],
            "Задание 2.4: готовая реализация torch.optim.RMSprop",
        )
        print()
        print("Пункт 4. Готовая реализация из PyTorch")
        print("Метод: torch.optim.RMSprop")
        print("Параметры: lr = 0.8, alpha = 0.99")
        print(f"Последняя точка: ({torch_result.final_point[0]:.8f}, {torch_result.final_point[1]:.8f})")
        print(f"Значение функции: {torch_result.final_value:.10f}")

    print()
    print("Вывод:")
    print("Обычный градиентный спуск может практически остановиться вблизи седловой точки,")
    print("потому что норма градиента становится очень маленькой. RMSProp позволяет")
    print("перераспределять шаг по координатам и за то же число итераций уйти к глобальному минимуму.")
    print()
    print(f"Графики сохранены в: {plots_dir.resolve()}")


if __name__ == "__main__":
    main()
