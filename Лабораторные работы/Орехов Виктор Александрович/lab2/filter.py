#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time
import os

import matplotlib
matplotlib.use('Agg') 

def apply_filter_F1(image, w, d):
    """Применяет фильтр F1 к изображению"""
    height, width = image.shape

    if w % 4 != 0:
        w = (w // 4) * 4

    x_coords = []
    y_values = []
    left_boundary = 0

    while left_boundary + w <= width:
        center_x = left_boundary + w / 2
        filter_region = image[:, left_boundary:left_boundary + w]
        half_width = w // 2
        left_half = filter_region[:, :half_width]
        right_half = filter_region[:, half_width:]

        sum_left = np.sum(left_half.astype(np.float64))
        sum_right = np.sum(right_half.astype(np.float64))
        y = sum_right - sum_left

        x_coords.append(center_x)
        y_values.append(y)
        left_boundary += d

    return np.array(x_coords), np.array(y_values)

def load_and_preprocess_image(image_path):
    """Загружает и предобрабатывает изображение"""
    img = Image.open(image_path)
    img_gray = img.convert('L')
    img_array = np.array(img_gray)
    return img_array

def demonstrate_filter_principle(image, w, d):
    """Демонстрирует принцип работы"""
    height, width = image.shape

    print(f"\nДЕМОНСТРАЦИЯ ПРИНЦИПА РАБОТЫ ФИЛЬТРА F1:")
    print(f"Параметры: w={w}, d={d}")
    print("=" * 60)

    positions = [width // 4, width // 2, 3 * width // 4]

    for i, demo_x in enumerate(positions):
        demo_left = max(0, demo_x - w/2)
        demo_right = min(width, demo_x + w/2)

        filter_region = image[:, int(demo_left):int(demo_right)]
        left_half = filter_region[:, :w//2]
        right_half = filter_region[:, w//2:]

        sum_left = np.sum(left_half.astype(np.float64))
        sum_right = np.sum(right_half.astype(np.float64))
        y_demo = sum_right - sum_left

        print(f"\nПример {i+1} (x={demo_x:.1f}):")
        print(f"  Область: [{demo_left:.1f}-{demo_right:.1f}]")
        print(f"  Левая половина сумма: {sum_left:.0f}")
        print(f"  Правая половина сумма: {sum_right:.0f}")
        print(f"  y(x) = {sum_right:.0f} - {sum_left:.0f} = {y_demo:.0f}")

        if y_demo > 1000:
            print("  → ПРАВАЯ ЧАСТЬ ТЕМНЕЕ")
        elif y_demo < -1000:
            print("  ← ЛЕВАЯ ЧАСТЬ ТЕМНЕЕ")
        elif y_demo > 0:
            print("  → правая часть немного темнее")
        elif y_demo < 0:
            print("  ← левая часть немного темнее")
        else:
            print("   равномерная яркость")

def display_results_table(x_coords, y_values, max_rows=15):
    """Отображает таблицу значений"""
    print(f"\nТАБЛИЦА ЗНАЧЕНИЙ y(x) = μ₁(x) (первые {max_rows} строк):")
    print("=" * 70)
    print(f"{'Итерация':^8} {'x':^10} {'y(x)':^12} {'Интерпретация':^25}")
    print("-" * 70)

    for i in range(min(max_rows, len(x_coords))):
        x = x_coords[i]
        y = y_values[i]

        if y > 1000:
            interpretation = "→ ТЕМНАЯ ПРАВАЯ"
        elif y > 0:
            interpretation = "→ темная правая"
        elif y < -1000:
            interpretation = "← ТЕМНАЯ ЛЕВАЯ"
        elif y < 0:
            interpretation = "← темная левая"
        else:
            interpretation = "равномерно"

        print(f"{i:^8} {x:^10.1f} {y:^12.0f} {interpretation:^25}")

    if len(x_coords) > max_rows:
        print(f"... (пропущено {len(x_coords) - max_rows} строк)")

    print(f"\nСТАТИСТИКА СИГНАЛА:")
    print(f"Всего точек: {len(x_coords)}")
    print(f"Диапазон x: [{x_coords[0]:.1f} - {x_coords[-1]:.1f}]")
    print(f"Минимум y: {np.min(y_values):.0f}")
    print(f"Максимум y: {np.max(y_values):.0f}")
    print(f"Среднее y: {np.mean(y_values):.0f}")
    print(f"Стандартное отклонение: {np.std(y_values):.0f}")

def create_and_save_plots(image, x_coords, y_values, w, d, image_name=""):
    """Создает и сохраняет графики в файлы"""
    print("\nСОЗДАНИЕ ГРАФИКОВ...")

    # Создаем папку для результатов, если её нет
    results_dir = "filter_results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    timestamp = int(time.time())

    # 1. Основной график: изображение + сигнал
    print("Создание основного графика...")
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Левая панель: изображение с разметкой
    ax1.imshow(image, cmap='gray')
    ax1.set_title(f'Исходное изображение\n{image_name}', fontsize=12)
    ax1.set_xlabel('Координата x (пиксели)')
    ax1.set_ylabel('Координата y (пиксели)')

    # Добавляем разметку положений фильтра
    sample_positions = [0, len(x_coords)//3, 2*len(x_coords)//3, -1]
    colors = ['green', 'orange', 'cyan', 'purple']
    labels = ['Начало', '1/3 пути', '2/3 пути', 'Конец']

    for i, pos in enumerate(sample_positions):
        if pos < len(x_coords):
            center = x_coords[pos]
            ax1.axvline(x=center, color=colors[i], linewidth=2, 
                       label=f'{labels[i]}: x={center:.1f}')

    ax1.legend(fontsize=9)

    # Правая панель: сигнал
    ax2.plot(x_coords, y_values, 'b-', linewidth=2, label='y(x) = μ₁(x)')
    ax2.fill_between(x_coords, y_values, where=y_values>0, alpha=0.3, color='blue', label='y>0 (правая темнее)')
    ax2.fill_between(x_coords, y_values, where=y_values<0, alpha=0.3, color='red', label='y<0 (левая темнее)')
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5, linewidth=1)

    # Добавляем сетку и настройки
    ax2.set_xlabel('Координата x центра фильтра', fontsize=11)
    ax2.set_ylabel('y(x) = Σправые - Σлевые', fontsize=11)
    ax2.set_title(f'Сигнал фильтра F1\nw={w}, d={d}, точек: {len(x_coords)}', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=10)

    plt.tight_layout()
    main_plot_path = f'{results_dir}/filter_main_result_{timestamp}.png'
    plt.savefig(main_plot_path, dpi=150, bbox_inches='tight')
    plt.close(fig1)

    # 2. График только сигнала (детальный)
    print("Создание детального графика сигнала...")
    fig2, ax = plt.subplots(figsize=(14, 6))

    ax.plot(x_coords, y_values, 'b-', linewidth=2.5, alpha=0.8)
    ax.fill_between(x_coords, y_values, alpha=0.2, color='blue')

    # Размечаем значимые точки
    y_std = np.std(y_values)
    significant_points = []
    for i in range(1, len(y_values)-1):
        if abs(y_values[i]) > y_std * 1.5:
            if y_values[i] > y_values[i-1] and y_values[i] > y_values[i+1]:
                significant_points.append(('max', i, y_values[i]))
            elif y_values[i] < y_values[i-1] and y_values[i] < y_values[i+1]:
                significant_points.append(('min', i, y_values[i]))

    # Отмечаем несколько самых значимых точек
    for point_type, idx, val in significant_points[:6]:
        color = 'red' if point_type == 'max' else 'green'
        marker = 'o' if point_type == 'max' else 's'
        ax.plot(x_coords[idx], val, color=color, marker=marker, markersize=8, 
               label=f'{"Максимум" if point_type == "max" else "Минимум"}')

    ax.axhline(y=0, color='black', linestyle='--', alpha=0.7, linewidth=1)
    ax.set_xlabel('Координата x центра фильтра', fontsize=12)
    ax.set_ylabel('y(x) = μ₁(x)', fontsize=12)
    ax.set_title(f'Детальный анализ сигнала фильтра F1\nw={w}, d={d}', fontsize=13)
    ax.grid(True, alpha=0.3)

    # Добавляем только уникальные labels для легенды
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    if by_label:
        ax.legend(by_label.values(), by_label.keys(), fontsize=10)

    plt.tight_layout()
    signal_plot_path = f'{results_dir}/filter_signal_detail_{timestamp}.png'
    plt.savefig(signal_plot_path, dpi=150, bbox_inches='tight')
    plt.close(fig2)

    # 3. Гистограмма распределения y(x)
    print("Создание гистограммы распределения...")
    fig3, ax = plt.subplots(figsize=(10, 6))

    n, bins, patches = ax.hist(y_values, bins=30, alpha=0.7, color='purple', 
                              edgecolor='black', density=True)

    # Добавляем статистические линии
    mean_y = np.mean(y_values)
    std_y = np.std(y_values)
    ax.axvline(mean_y, color='red', linestyle='--', linewidth=2, 
              label=f'Среднее: {mean_y:.0f}')
    ax.axvline(mean_y + std_y, color='orange', linestyle=':', linewidth=1.5,
              label=f'±σ: {std_y:.0f}')
    ax.axvline(mean_y - std_y, color='orange', linestyle=':', linewidth=1.5)
    ax.axvline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)

    ax.set_xlabel('y(x) = μ₁(x)', fontsize=12)
    ax.set_ylabel('Плотность вероятности', fontsize=12)
    ax.set_title('Распределение значений y(x)', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    hist_plot_path = f'{results_dir}/filter_histogram_{timestamp}.png'
    plt.savefig(hist_plot_path, dpi=150, bbox_inches='tight')
    plt.close(fig3)

    print(f"\n  ГРАФИКИ УСПЕШНО СОХРАНЕНЫ:")
    print(f"    Основной результат: {main_plot_path}")
    print(f"    Детальный сигнал: {signal_plot_path}")
    print(f"    Гистограмма: {hist_plot_path}")
    print(f"\n  Все файлы сохранены в папку: {results_dir}/")

def analyze_signal_features(x_coords, y_values):
    """Анализирует особенности сигнала"""
    print(f"\nАНАЛИЗ ОСОБЕННОСТЕЙ СИГНАЛА:")
    print("-" * 50)

    y_mean = np.mean(y_values)
    y_std = np.std(y_values)
    zero_crossings = np.where(np.diff(np.signbit(y_values)))[0]

    # Находим экстремумы
    maxima = []
    minima = []
    for i in range(1, len(y_values)-1):
        if y_values[i] > y_values[i-1] and y_values[i] > y_values[i+1]:
            maxima.append(i)
        elif y_values[i] < y_values[i-1] and y_values[i] < y_values[i+1]:
            minima.append(i)

    print(f"Среднее значение y(x): {y_mean:.0f}")
    print(f"Стандартное отклонение: {y_std:.0f}")
    print(f"Количество нулевых пересечений: {len(zero_crossings)}")
    print(f"Локальных максимумов: {len(maxima)}")
    print(f"Локальных минимумов: {len(minima)}")

    # Интерпретация
    print(f"\nИНТЕРПРЕТАЦИЯ РЕЗУЛЬТАТОВ:")
    if abs(y_mean) < y_std * 0.3:
        print("• Изображение имеет сбалансированное распределение яркости")
    elif y_mean > 0:
        print("• Преобладают области с более темной правой половиной")
    else:
        print("• Преобладают области с более темной левой половиной")

    if len(zero_crossings) > len(y_values) * 0.2:
        print("• Частые переходы через ноль указывают на сложную структуру изображения")

    significant_extrema = len([y for y in y_values if abs(y) > y_std * 1.5])
    print(f"• Значимых экстремумов (>1.5σ): {significant_extrema}")

# Основная программа
if __name__ == "__main__":
    try:
        # Параметры фильтра
        w = 16
        d = 2
        image_path = "/home/user/Work/Averbuh/lab2/07.jpg"

        print("=" * 80)
        print("ЛАБОРАТОРНАЯ РАБОТА: ФИЛЬТР F1 ТЕОРИИ АКТИВНОГО ВОСПРИЯТИЯ")
        print("=" * 80)

        # 1. Загрузка изображения
        print("\n1. ЗАГРУЗКА И ПОДГОТОВКА ИЗОБРАЖЕНИЯ")
        image = load_and_preprocess_image(image_path)
        print(f"   Размер изображения: {image.shape[1]} x {image.shape[0]} пикселей")
        print(f"   Диапазон яркости: [{np.min(image)} - {np.max(image)}]")

        # 2. Демонстрация принципа работы
        print("\n2. ДЕМОНСТРАЦИЯ ПРИНЦИПА РАБОТЫ ФИЛЬТРА")
        demonstrate_filter_principle(image, w, d)

        # 3. Применение фильтра
        print("\n3. ПРИМЕНЕНИЕ ФИЛЬТРА F1 КО ВСЕМУ ИЗОБРАЖЕНИЮ")
        x_coords, y_values = apply_filter_F1(image, w, d)

        # 4. Таблица результатов
        print("\n4. ТАБЛИЦА РЕЗУЛЬТАТОВ")
        display_results_table(x_coords, y_values)

        # 5. Анализ сигнала
        print("\n5. АНАЛИЗ СИГНАЛА")
        analyze_signal_features(x_coords, y_values)

        # 6. Создание графиков (только сохранение в файлы)
        print("\n6. СОЗДАНИЕ И СОХРАНЕНИЕ ГРАФИКОВ")
        create_and_save_plots(image, x_coords, y_values, w, d, "Анализ изображения")

        print("\n" + "=" * 80)
        print("ЛАБОРАТОРНАЯ РАБОТА УСПЕШНО ЗАВЕРШЕНА!")
        print("=" * 80)
        print("Результаты сохранены в папку 'filter_results/'")
        print("Для просмотра графиков откройте сохраненные PNG-файлы")

    except FileNotFoundError:
        print("\n ОШИБКА: Файл изображения не найден!")
        print(f"   Проверьте путь: {image_path}")

    except Exception as e:
        print(f"\n ОШИБКА: {e}")
        import traceback
        traceback.print_exc()