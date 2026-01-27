# Примеры использования String Art Generator

## Базовое использование

```bash
# Активировать виртуальное окружение (если используется)
source .venv/bin/activate

# Запустить генератор
python string_art.py image.png
```

## Примеры настройки параметров

### Быстрый результат (2-3 часа работы)

Отредактируйте `string_art.py`:
```python
NUM_NAILS = 150
NUM_STEPS = 2000
TARGET_SIZE = 600
```

### Стандартный результат (4-5 часов работы) - по умолчанию

```python
NUM_NAILS = 180
NUM_STEPS = 3500
TARGET_SIZE = 800
```

### Высокое качество (6-8 часов работы)

```python
NUM_NAILS = 200
NUM_STEPS = 4500
TARGET_SIZE = 1000
THREAD_STRENGTH = 0.20
```

### Очень детальный (10+ часов работы)

```python
NUM_NAILS = 250
NUM_STEPS = 6000
TARGET_SIZE = 1200
THREAD_STRENGTH = 0.18
```

## Настройка для разных типов изображений

### Портреты

```python
INVERT_IMAGE = True
THREAD_STRENGTH = 0.22
NUM_NAILS = 200
```

### Логотипы и простые формы

```python
INVERT_IMAGE = True
THREAD_STRENGTH = 0.25
NUM_NAILS = 150
NUM_STEPS = 2500
```

### Высококонтрастные изображения

```python
INVERT_IMAGE = True
THREAD_STRENGTH = 0.18
LINE_WEIGHT = 10
```

### Низкоконтрастные изображения

```python
INVERT_IMAGE = True
THREAD_STRENGTH = 0.28
LINE_WEIGHT = 14
```

## Настройка размера бумаги

### A4 формат (210×297 мм)

```python
A3_WIDTH_MM = 210
A3_HEIGHT_MM = 297
A3_WIDTH_IN = 8.27
A3_HEIGHT_IN = 11.69
MARGIN_MM = 25
WORKING_AREA_MM = min(A3_WIDTH_MM, A3_HEIGHT_MM) - 2 * MARGIN_MM
CIRCLE_RADIUS_MM = WORKING_AREA_MM / 2
```

### A2 формат (420×594 мм)

```python
A3_WIDTH_MM = 420
A3_HEIGHT_MM = 594
A3_WIDTH_IN = 16.54
A3_HEIGHT_IN = 23.39
MARGIN_MM = 50
WORKING_AREA_MM = min(A3_WIDTH_MM, A3_HEIGHT_MM) - 2 * MARGIN_MM
CIRCLE_RADIUS_MM = WORKING_AREA_MM / 2
```

## Настройка внешнего вида нумерации

### Крупная нумерация (для больших форматов)

```python
NAIL_NUMBER_FONT_SIZE_BASE = 18
NAIL_NUMBER_OFFSET_MM = 10
HIGHLIGHT_EVERY_NTH_NAIL = 10
```

### Мелкая нумерация (для малых форматов)

```python
NAIL_NUMBER_FONT_SIZE_BASE = 10
NAIL_NUMBER_OFFSET_MM = 6
HIGHLIGHT_EVERY_NTH_NAIL = 15
```

## Пакетная обработка

Создайте скрипт `batch_process.sh`:

```bash
#!/bin/bash

for img in input_images/*.png; do
    echo "Processing $img..."
    python string_art.py "$img"
    
    # Переместить результаты в папку с именем файла
    basename=$(basename "$img" .png)
    mkdir -p "output/$basename"
    mv nails_scheme.* instructions.csv drawing_simulation.* "output/$basename/"
done
```

## Советы по оптимизации

### Если программа работает слишком долго

1. Уменьшите `TARGET_SIZE` до 600-700
2. Уменьшите `NUM_STEPS` до 2500-3000
3. Убедитесь что `AUTO_STOP = True`

### Если результат слишком тёмный

1. Уменьшите `THREAD_STRENGTH` на 0.02-0.05
2. Уменьшите `NUM_STEPS` на 500-1000

### Если результат слишком светлый

1. Увеличьте `THREAD_STRENGTH` на 0.02-0.05
2. Увеличьте `NUM_STEPS` на 500-1000

### Если нумерация гвоздей плохо читается

1. Увеличьте `NAIL_NUMBER_FONT_SIZE_BASE`
2. Увеличьте `NAIL_NUMBER_OFFSET_MM`
3. Уменьшите `NUM_NAILS` для большего расстояния между гвоздями

## Проверка результатов

После генерации проверьте:
1. `drawing_simulation.png` - так будет выглядеть результат
2. `nails_scheme.png` - читаемость номеров гвоздей
3. `instructions.csv` - длина нити (убедитесь, что у вас достаточно)

## Устранение проблем

### Ошибка "ModuleNotFoundError"

```bash
pip install -r requirements.txt
# или
python -m pip install -r requirements.txt
```

### Ошибка памяти

Уменьшите параметры:
```python
TARGET_SIZE = 600
NUM_STEPS = 2000
```

### Изображение не загружается

Убедитесь что:
- Файл существует
- Формат поддерживается (JPG, PNG, BMP)
- Путь к файлу указан правильно

### Слишком большой PDF

PDF файлы могут быть большими (50-100 МБ) при 300 DPI.
Для уменьшения размера можно:
- Использовать только PNG файлы (отключить PDF)
- Уменьшить `SCHEME_DPI` до 150-200

```python
EXPORT_SCHEME_PDF = False  # Отключить PDF
SCHEME_DPI = 200  # Уменьшить разрешение
```
