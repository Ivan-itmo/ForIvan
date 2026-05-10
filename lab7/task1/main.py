from __future__ import annotations

import os
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


BOX = (-4.0, 4.0, -4.0, 4.0)
SADDLE = np.array([-1.0, 2.5], dtype=float)
GLOBAL_MIN = np.array([-3.0 / 16.0, -4.0], dtype=float)


def f(point: np.ndarray) -> float:
    x, y = point
    return 1e-2 * (8 * x * x + 2 * x * y + 11 * x + 2 * y + 3)


def hessian() -> np.ndarray:
    return 1e-2 * np.array([[16.0, 2.0], [2.0, 0.0]], dtype=float)


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


def plot_contours(output: Path) -> None:
    xx, yy, zz = make_grid(BOX[:2], BOX[2:])
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
    )
    plt.scatter(*SADDLE, color="red", s=70, marker="x", label="седловая точка")
    plt.scatter(*GLOBAL_MIN, color="green", s=70, marker="*", label="глобальный минимум")
    plt.xlim(*BOX[:2])
    plt.ylim(*BOX[2:])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Задание 1: линии уровня функции в области Omega")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output, dpi=180)
    plt.close()


def main() -> None:
    plots_dir = ROOT / "plots"
    plots_dir.mkdir(exist_ok=True)
    plot_contours(plots_dir / "levels.png")

    eigenvalues = np.linalg.eigvalsh(hessian())

    print("Задание 1")
    print("==========")
    print("Исследуемая функция:")
    print("f(x, y) = 10^(-2) * (8x^2 + 2xy + 11x + 2y + 3)")
    print()
    print(f"Область исследования: Omega = [{BOX[0]}, {BOX[1]}] x [{BOX[2]}, {BOX[3]}]")
    print()
    print("Стационарная точка:")
    print(f"(x*, y*) = ({SADDLE[0]}, {SADDLE[1]})")
    print()
    print("Гессиан:")
    print("[[0.16, 0.02],")
    print(" [0.02, 0.00]]")
    print(f"Собственные значения гессиана: {eigenvalues}")
    print("Так как собственные значения имеют разные знаки, гессиан неопределён.")
    print("Следовательно, точка (-1, 2.5) является седловой.")
    print()
    print("Локальные экстремумы:")
    print("Локальных минимумов и максимумов внутри области Omega нет.")
    print()
    print("Глобальный минимум в заданной области:")
    print(f"(x_min, y_min) = ({GLOBAL_MIN[0]}, {GLOBAL_MIN[1]})")
    print(f"f(x_min, y_min) = {f(GLOBAL_MIN):.7f}")
    print()
    print("Вывод:")
    print("Линии уровня показывают, что около седловой точки градиентный спуск может")
    print("двигаться очень медленно и создавать иллюзию сходимости, хотя глобальный минимум")
    print("находится на границе области.")
    print()
    print(f"График сохранён в: {(plots_dir / 'levels.png').resolve()}")


if __name__ == "__main__":
    main()
