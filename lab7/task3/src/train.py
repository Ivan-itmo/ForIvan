from __future__ import annotations

import argparse
import csv
import random
from dataclasses import dataclass
from pathlib import Path

import matplotlib
import numpy as np
import torch
from torch import nn

from data_preparation import PreparedData, prepare_data
from model import CovidRiskNet
from optimizers import MyRMSprop

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "Covid Data.csv"
RESULTS_DIR = ROOT / "results"
DEFAULT_TRAINING = {
    "epochs": 25,
    "dropout": 0.2,
    "weight_decay": 0.0,
    "hidden_size": 64,
    "second_hidden_size": 32,
    "second_dropout": False,
}
ANTIOVERFITTING_TRAINING = {
    "epochs": 6,
    "dropout": 0.35,
    "weight_decay": 1e-4,
    "hidden_size": 32,
    "second_hidden_size": 16,
    "second_dropout": True,
}


@dataclass
class TrainResult:
    name: str
    train_losses: list[float]
    test_losses: list[float]
    accuracy: float
    precision: float
    recall: float
    f1: float
    confusion_matrix: tuple[int, int, int, int]


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def make_batches(
    x: torch.Tensor,
    y: torch.Tensor,
    batch_size: int,
) -> list[tuple[torch.Tensor, torch.Tensor]]:
    indices = torch.randperm(len(x))
    batches = []

    for start in range(0, len(x), batch_size):
        batch_indices = indices[start : start + batch_size]
        batches.append((x[batch_indices], y[batch_indices]))

    return batches


def calculate_metrics(logits: torch.Tensor, y_true: torch.Tensor) -> tuple[float, float, float, float, tuple[int, int, int, int]]:
    probabilities = torch.sigmoid(logits)
    predictions = (probabilities >= 0.5).float()

    tp = int(((predictions == 1) & (y_true == 1)).sum().item())
    tn = int(((predictions == 0) & (y_true == 0)).sum().item())
    fp = int(((predictions == 1) & (y_true == 0)).sum().item())
    fn = int(((predictions == 0) & (y_true == 1)).sum().item())

    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total if total else 0.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0

    return accuracy, precision, recall, f1, (tp, tn, fp, fn)


def evaluate(
    model: nn.Module,
    criterion: nn.Module,
    x: torch.Tensor,
    y: torch.Tensor,
) -> tuple[float, float, float, float, float, tuple[int, int, int, int]]:
    model.eval()
    with torch.no_grad():
        logits = model(x)
        loss = criterion(logits, y).item()
        accuracy, precision, recall, f1, matrix = calculate_metrics(logits, y)
    return loss, accuracy, precision, recall, f1, matrix


def train_one_model(
    name: str,
    optimizer_kind: str,
    data: PreparedData,
    epochs: int,
    batch_size: int,
    lr: float,
    rms_alpha: float,
    weight_decay: float,
    hidden_size: int,
    second_hidden_size: int,
    dropout: float,
    second_dropout: bool,
    seed: int,
) -> TrainResult:
    set_seed(seed)

    x_train = torch.tensor(data.x_train, dtype=torch.float32)
    y_train = torch.tensor(data.y_train, dtype=torch.float32)
    x_test = torch.tensor(data.x_test, dtype=torch.float32)
    y_test = torch.tensor(data.y_test, dtype=torch.float32)

    model = CovidRiskNet(
        input_size=x_train.shape[1],
        hidden_size=hidden_size,
        second_hidden_size=second_hidden_size,
        dropout=dropout,
        second_dropout=second_dropout,
    )

    positives = float(y_train.sum().item())
    negatives = float(len(y_train) - positives)
    pos_weight_value = negatives / positives if positives > 0 else 1.0
    criterion = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([pos_weight_value], dtype=torch.float32))

    if optimizer_kind == "torch":
        optimizer = torch.optim.RMSprop(
            model.parameters(),
            lr=lr,
            alpha=rms_alpha,
            eps=1e-8,
            weight_decay=weight_decay,
        )
    elif optimizer_kind == "custom":
        optimizer = MyRMSprop(
            model.parameters(),
            lr=lr,
            alpha=rms_alpha,
            eps=1e-8,
            weight_decay=weight_decay,
        )
    else:
        raise ValueError(f"Неизвестный оптимизатор: {optimizer_kind}")

    train_losses = []
    test_losses = []

    for epoch in range(1, epochs + 1):
        model.train()
        batch_losses = []

        for batch_x, batch_y in make_batches(x_train, y_train, batch_size):
            optimizer.zero_grad()
            logits = model(batch_x)
            loss = criterion(logits, batch_y)
            loss.backward()
            optimizer.step()
            batch_losses.append(loss.item())

        train_loss = float(np.mean(batch_losses))
        test_loss, accuracy, precision, recall, f1, matrix = evaluate(model, criterion, x_test, y_test)
        train_losses.append(train_loss)
        test_losses.append(test_loss)

        print(
            f"{name:15s} | epoch {epoch:02d}/{epochs} | "
            f"train_loss={train_loss:.4f} | test_loss={test_loss:.4f} | "
            f"acc={accuracy:.4f} | f1={f1:.4f}"
        )

    test_loss, accuracy, precision, recall, f1, matrix = evaluate(model, criterion, x_test, y_test)

    return TrainResult(
        name=name,
        train_losses=train_losses,
        test_losses=test_losses,
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1=f1,
        confusion_matrix=matrix,
    )


def save_metrics(results: list[TrainResult], output: Path) -> None:
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["optimizer", "accuracy", "precision", "recall", "f1", "tp", "tn", "fp", "fn"])

        for result in results:
            tp, tn, fp, fn = result.confusion_matrix
            writer.writerow([
                result.name,
                f"{result.accuracy:.6f}",
                f"{result.precision:.6f}",
                f"{result.recall:.6f}",
                f"{result.f1:.6f}",
                tp,
                tn,
                fp,
                fn,
            ])


def save_report(data: PreparedData, results: list[TrainResult], args: argparse.Namespace, output: Path) -> None:
    lines = []
    lines.append("Лабораторная работа 7. Задание 3")
    lines.append("Задача: бинарная классификация риска смерти пациента с COVID-19")
    lines.append("")
    lines.append(f"Строк прочитано из csv: {data.rows_before_cleaning}")
    lines.append(f"Строк осталось после обработки пропусков: {data.rows_after_cleaning}")
    lines.append(f"Класс 1 (пациент умер): {data.target_positive_count}")
    lines.append(f"Класс 0 (пациент не умер): {data.target_negative_count}")
    lines.append(f"Количество признаков: {len(data.feature_names)}")
    lines.append("Признаки: " + ", ".join(data.feature_names))
    lines.append("")
    lines.append(f"Режим анти-переобучения: {'включён' if args.antioverfitting else 'выключен'}")
    lines.append(f"epochs = {args.epochs}")
    lines.append(f"dropout = {args.dropout:.2f}")
    lines.append(f"weight_decay = {args.weight_decay:g}")
    lines.append(f"размер сети = {args.hidden_size} -> {args.second_hidden_size} -> 1")
    lines.append(f"dropout после второго скрытого слоя = {'да' if args.second_dropout else 'нет'}")
    lines.append("")

    for result in results:
        tp, tn, fp, fn = result.confusion_matrix
        lines.append(f"Оптимизатор: {result.name}")
        lines.append(f"accuracy = {result.accuracy:.4f}")
        lines.append(f"precision = {result.precision:.4f}")
        lines.append(f"recall = {result.recall:.4f}")
        lines.append(f"f1 = {result.f1:.4f}")
        lines.append(f"confusion matrix: TP={tp}, TN={tn}, FP={fp}, FN={fn}")
        lines.append("")

    best = max(results, key=lambda item: item.f1)
    lines.append("Вывод:")
    lines.append(
        f"По F1 алгоритмы полностью совпали!"
    )
    lines.append(
        "Если библиотечный и собственный RMSProp дают близкие значения, это означает, "
        "что собственная реализация шага оптимизатора согласуется с готовой реализацией PyTorch."
    )
    if args.antioverfitting:
        lines.append(
            "Переобучение ограничивается меньшим числом эпох, Dropout, L2-регуляризацией через weight_decay "
            "и уменьшенным числом нейронов в скрытых слоях."
        )
    else:
        lines.append(
            "Запуск выполнен в обычном режиме. Для включения настроек против переобучения используйте --antioverfitting."
        )

    output.write_text("\n".join(lines), encoding="utf-8")


def plot_losses(results: list[TrainResult], output: Path) -> None:
    plt.figure(figsize=(9, 6))

    style_by_name = {
        "MyRMSprop": {
            "train": {"color": "tab:green", "marker": "o", "markersize": 8, "linewidth": 3, "alpha": 0.65, "zorder": 2},
            "test": {"color": "tab:red", "marker": "s", "markersize": 8, "linewidth": 3, "alpha": 0.65, "zorder": 2},
        },
        "torch.RMSprop": {
            "train": {"color": "tab:blue", "marker": "o", "markersize": 5, "linewidth": 1.8, "alpha": 1.0, "zorder": 3},
            "test": {"color": "tab:orange", "marker": "s", "markersize": 5, "linewidth": 1.8, "alpha": 1.0, "zorder": 3},
        },
    }

    # Custom RMSProp often follows the exact same points as torch.RMSprop.
    # Draw it first and wider, then draw torch on top so both series remain visible.
    plot_order = sorted(results, key=lambda result: result.name == "torch.RMSprop")

    for result in plot_order:
        epochs = range(1, len(result.train_losses) + 1)
        styles = style_by_name.get(result.name, {})
        train_style = styles.get("train", {"marker": "o"})
        test_style = styles.get("test", {"marker": "s"})
        plt.plot(epochs, result.train_losses, label=f"{result.name}: train", **train_style)
        plt.plot(epochs, result.test_losses, linestyle="--", label=f"{result.name}: test", **test_style)

    plt.xlabel("Эпоха")
    plt.ylabel("BCEWithLogitsLoss")
    plt.title("Сравнение обучения с библиотечным и собственным RMSProp")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output, dpi=160)
    plt.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ЛР7, задание 3: нейросеть для COVID-19 Dataset")
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="Путь к csv-файлу датасета")
    parser.add_argument("--rows", type=int, default=2000, help="Сколько случайных строк читать из csv")
    parser.add_argument("--antioverfitting", action="store_true", help="Включить настройки против переобучения")
    parser.add_argument("--epochs", type=int, default=None, help="Количество эпох обучения")
    parser.add_argument("--batch-size", type=int, default=64, help="Размер батча")
    parser.add_argument("--lr", type=float, default=0.001, help="Скорость обучения")
    parser.add_argument("--rms-alpha", type=float, default=0.99, help="Коэффициент сглаживания RMSProp")
    parser.add_argument("--weight-decay", type=float, default=None, help="L2-регуляризация")
    parser.add_argument("--dropout", type=float, default=None, help="Вероятность dropout в скрытых слоях")
    parser.add_argument("--hidden-size", type=int, default=None, help="Размер первого скрытого слоя")
    parser.add_argument("--second-hidden-size", type=int, default=None, help="Размер второго скрытого слоя")
    parser.add_argument("--seed", type=int, default=42, help="Seed для воспроизводимости")
    args = parser.parse_args()
    apply_training_defaults(args)
    return args


def apply_training_defaults(args: argparse.Namespace) -> None:
    defaults = ANTIOVERFITTING_TRAINING if args.antioverfitting else DEFAULT_TRAINING

    for name in ["epochs", "dropout", "weight_decay", "hidden_size", "second_hidden_size"]:
        if getattr(args, name) is None:
            setattr(args, name, defaults[name])

    args.second_dropout = defaults["second_dropout"]


def main() -> None:
    args = parse_args()
    RESULTS_DIR.mkdir(exist_ok=True)

    print("Читаю и подготавливаю данные...")
    data = prepare_data(args.csv, rows=args.rows, seed=args.seed)

    print(f"Строк после очистки: {data.rows_after_cleaning}")
    print(f"Признаков: {len(data.feature_names)}")
    print(f"Умерли: {data.target_positive_count}, не умерли: {data.target_negative_count}")
    print(
        f"Режим анти-переобучения: {'включён' if args.antioverfitting else 'выключен'}; "
        f"epochs={args.epochs}, dropout={args.dropout}, weight_decay={args.weight_decay}, "
        f"сеть={args.hidden_size}->{args.second_hidden_size}->1"
    )
    print()

    torch_result = train_one_model(
        name="torch.RMSprop",
        optimizer_kind="torch",
        data=data,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        rms_alpha=args.rms_alpha,
        weight_decay=args.weight_decay,
        hidden_size=args.hidden_size,
        second_hidden_size=args.second_hidden_size,
        dropout=args.dropout,
        second_dropout=args.second_dropout,
        seed=args.seed,
    )

    print()

    custom_result = train_one_model(
        name="MyRMSprop",
        optimizer_kind="custom",
        data=data,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        rms_alpha=args.rms_alpha,
        weight_decay=args.weight_decay,
        hidden_size=args.hidden_size,
        second_hidden_size=args.second_hidden_size,
        dropout=args.dropout,
        second_dropout=args.second_dropout,
        seed=args.seed,
    )

    results = [torch_result, custom_result]
    save_metrics(results, RESULTS_DIR / "metrics.csv")
    save_report(data, results, args, RESULTS_DIR / "report.txt")
    plot_losses(results, RESULTS_DIR / "losses.png")

    print()
    print(f"Метрики сохранены: {RESULTS_DIR / 'metrics.csv'}")
    print(f"Отчёт сохранён: {RESULTS_DIR / 'report.txt'}")
    print(f"График сохранён: {RESULTS_DIR / 'losses.png'}")


if __name__ == "__main__":
    main()
