# Task 2

Здесь лежит численное решение второго задания.

## Назначение файлов

- [main.py](/Users/ivan/Desktop/MetOpt/lab7/task2/main.py) — расчёты, параметры методов, число итераций и текстовые выводы.
- [Contours and solutions.ipynb](/Users/ivan/Desktop/MetOpt/lab7/task2/Contours%20and%20solutions.ipynb) — построение графиков и визуализация траекторий.

## Что должно получиться

- обычный градиентный спуск, который приближается к седловой точке;
- `RMSProp`, который за то же число итераций преодолевает окрестность седловой точки;
- сравнение двух наборов гиперпараметров `RMSProp`;
- вариант с готовой реализацией `torch.optim.RMSprop`.

## Актуальные графики

- `plots/gd_to_saddle.png`
- `plots/rmsprop_escape.png`
- `plots/hyperparams_compare.png`
- `plots/torch_rmsprop.png`

## Запуск

Расчёты:

```bash
../.venv/bin/python main.py
```

Графики:

Откройте `Contours and solutions.ipynb` и выполните ячейки ноутбука.
