# Префіксне дерево (Trie) — розширення функціоналу

## Мета

Реалізувати два методи в класі `Homework` (успадкований від `Trie`):

- `count_words_with_suffix(pattern)` — повертає кількість слів, що **закінчуються** на `pattern`;
- `has_prefix(prefix)` — перевіряє, чи існує хоча б одне слово з префіксом `prefix`.

## Важливі технічні деталі

- `Homework` успадковує `Trie` (файл: `src/trie.py`).
- Обидва вхідні параметри мають бути `str`; інакше піднімається `TypeError`.
- `count_words_with_suffix` повертає `int`.
- `has_prefix` повертає `bool`.
- За порожній рядок: `count_words_with_suffix("")` — рахує всі слова; `has_prefix("")` — True якщо є хоча б одне слово.

## Поведінка та приклади

```py
>>> from src.trie import Homework
>>> t = Homework()
>>> for w in ("app", "apple", "application", "cat"):
...     t.insert(w)
>>> t.count_words_with_suffix("le")
1
>>> t.count_words_with_suffix("")
4
>>> t.has_prefix("app")
True
>>> t.has_prefix("z")
False
```

## Тести

- Розміщено в `tests/test_trie.py` — покривають коректність, типи повернення та валідацію вхідних даних.

## Як запустити тестування

1. Перейти в папку `task-2`
2. Встановити залежності (рекомендується віртуальне середовище):
   ```bash
   pip install -r requirements.txt
   ```
3. Запустити:
   ```bash
   pytest -q
   ```
