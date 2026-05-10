# Lab 7

Проект разложен по трём отдельным папкам:

- [task1](/Users/ivan/Desktop/MetOpt/lab7/task1) — аналитическое исследование функции и линии уровня.
- [task2](/Users/ivan/Desktop/MetOpt/lab7/task2) — обычный градиентный спуск, momentum / heavy-ball, сравнение гиперпараметров и вариант на PyTorch.
- [task3](/Users/ivan/Desktop/MetOpt/lab7/task3) — шаблон под третье задание с нейросетью и датасетом.

Для заданий 1 и 2 используется функция

\[
f(x, y) = 10^{-2} (8x^2 + 2xy + 11x + 2y + 3)
\]

и область

\[
\Omega = [-4, 4] \times [-4, 4].
\]

Это допущение сохранено, потому что в исходной постановке была указана только функция, без границ области.

## Быстрый запуск

```bash
cd task1 && ../.venv/bin/python main.py
cd task2 && ../.venv/bin/python main.py
cd task3 && ../.venv/bin/python main.py
```
