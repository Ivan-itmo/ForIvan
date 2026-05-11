from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


TARGET_COLUMN = "DATE_DIED"

BOOLEAN_COLUMNS_WITH_98_AS_MISSING = [
    "DIABETES",
    "COPD",
    "ASTHMA",
    "INMSUPR",
    "HIPERTENSION",
    "OTHER_DISEASE",
    "CARDIOVASCULAR",
    "OBESITY",
    "RENAL_CHRONIC",
    "TOBACCO",
]

FEATURE_COLUMNS = [
    "USMER",
    "MEDICAL_UNIT",
    "SEX",
    "PATIENT_TYPE",
    "INTUBED",
    "PNEUMONIA",
    "AGE",
    "PREGNANT",
    "DIABETES",
    "COPD",
    "ASTHMA",
    "INMSUPR",
    "HIPERTENSION",
    "OTHER_DISEASE",
    "CARDIOVASCULAR",
    "OBESITY",
    "RENAL_CHRONIC",
    "TOBACCO",
    "CLASIFFICATION_FINAL",
    "ICU",
]


@dataclass
class PreparedData:
    x_train: np.ndarray
    y_train: np.ndarray
    x_test: np.ndarray
    y_test: np.ndarray
    feature_names: list[str]
    rows_before_cleaning: int
    rows_after_cleaning: int
    target_positive_count: int
    target_negative_count: int


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [name.strip().upper().replace(" ", "_") for name in df.columns]
    return df


def read_dataset(csv_path: Path, rows: int, seed: int) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Файл {csv_path} не найден. Положите csv в папку data или передайте путь через --csv."
        )

    df = normalize_column_names(pd.read_csv(csv_path))
    check_columns(df)

    if rows < len(df):
        df = df.sample(n=rows, random_state=seed)

    return df.reset_index(drop=True)


def make_target(df: pd.DataFrame) -> pd.Series:
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"В датасете нет столбца {TARGET_COLUMN}")

    # 9999-99-99 означает, что пациент не умер.
    return (df[TARGET_COLUMN].astype(str) != "9999-99-99").astype(np.float32)


def fix_context_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # В датасете 1 = yes, 2 = no.
    # Мужчина не может быть беременным: для SEX=2 значение PREGNANT=97 заменяем на 2.
    if {"SEX", "PREGNANT"}.issubset(df.columns):
        mask_male_pregnant_97 = (df["SEX"] == 2) & (df["PREGNANT"] == 97)
        df.loc[mask_male_pregnant_97, "PREGNANT"] = 2

    # Если пациента отправили домой, он не попадал в ICU и не был интубирован.
    if "PATIENT_TYPE" in df.columns:
        for column in ["ICU", "INTUBED"]:
            if column in df.columns:
                mask_home_97 = (df["PATIENT_TYPE"] == 1) & (df[column] == 97)
                df.loc[mask_home_97, column] = 2

    return df


def drop_missing_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # После контекстных замен оставшиеся 97 в этих колонках считаем пропусками.
    for column in ["PREGNANT", "ICU", "INTUBED"]:
        if column in df.columns:
            df.loc[df[column].isin([97, 98, 99]), column] = np.nan

    if "PNEUMONIA" in df.columns:
        df.loc[df["PNEUMONIA"].isin([99]), "PNEUMONIA"] = np.nan

    for column in BOOLEAN_COLUMNS_WITH_98_AS_MISSING:
        if column in df.columns:
            df.loc[df[column].isin([98]), column] = np.nan

    return df.dropna().reset_index(drop=True)


def check_columns(df: pd.DataFrame) -> None:
    missing = [column for column in FEATURE_COLUMNS + [TARGET_COLUMN] if column not in df.columns]
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"В csv не хватает нужных столбцов: {joined}")


def stratified_split(
    x: np.ndarray,
    y: np.ndarray,
    test_size: float = 0.2,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    train_parts = []
    test_parts = []

    for class_value in np.unique(y):
        indices = np.where(y == class_value)[0]
        rng.shuffle(indices)
        test_count = max(1, int(len(indices) * test_size))
        test_parts.append(indices[:test_count])
        train_parts.append(indices[test_count:])

    train_indices = np.concatenate(train_parts)
    test_indices = np.concatenate(test_parts)
    rng.shuffle(train_indices)
    rng.shuffle(test_indices)

    return x[train_indices], y[train_indices], x[test_indices], y[test_indices]


def standardize(
    x_train: np.ndarray,
    x_test: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    mean = x_train.mean(axis=0)
    std = x_train.std(axis=0)
    std[std == 0] = 1.0

    return (x_train - mean) / std, (x_test - mean) / std


def prepare_data(csv_path: Path, rows: int, seed: int = 42) -> PreparedData:
    df = read_dataset(csv_path, rows, seed)

    rows_before_cleaning = len(df)
    df = fix_context_values(df)
    y = make_target(df)

    df = df[FEATURE_COLUMNS].copy()
    df["TARGET"] = y
    df = drop_missing_rows(df)

    if len(df) < 100:
        raise ValueError(
            "После удаления пропусков осталось меньше 100 объектов. "
            "Увеличьте --rows, например до 5000 или 10000."
        )

    y = df["TARGET"].to_numpy(dtype=np.float32)
    if len(np.unique(y)) < 2:
        raise ValueError(
            "В выбранных строках есть только один класс target. "
            "Для обучения бинарной классификации нужны и умершие, и выжившие пациенты. "
            "Увеличьте --rows."
        )

    x = df[FEATURE_COLUMNS].to_numpy(dtype=np.float32)
    x_train, y_train, x_test, y_test = stratified_split(x, y, seed=seed)
    x_train, x_test = standardize(x_train, x_test)

    return PreparedData(
        x_train=x_train.astype(np.float32),
        y_train=y_train.astype(np.float32),
        x_test=x_test.astype(np.float32),
        y_test=y_test.astype(np.float32),
        feature_names=FEATURE_COLUMNS,
        rows_before_cleaning=rows_before_cleaning,
        rows_after_cleaning=len(df),
        target_positive_count=int(y.sum()),
        target_negative_count=int(len(y) - y.sum()),
    )
