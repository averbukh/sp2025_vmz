import numpy as np
import matplotlib.pyplot as plt

def get_user_input():
    """Запрашивает у пользователя входные данные и возвращает их."""
    print("=== Программа для расчета зависимости y(x) ===")
    a1 = float(input("Введите коэффициент a1 (амплитуда первой синусоиды): "))
    b1 = float(input("Введите коэффициент b1 (частота первой синусоиды): "))
    a2 = float(input("Введите коэффициент a2 (амплитуда второй синусоиды): "))
    b2 = float(input("Введите коэффициент b2 (частота второй синусоиды): "))
    a3 = float(input("Введите коэффициент a3 (амплитуда третьей синусоиды): "))
    b3 = float(input("Введите коэффициент b3 (частота третьей синусоиды): "))
    x0 = float(input("Введите начальное значение x (x0): "))
    xk = float(input("Введите конечное значение x (xk): "))
    dx = float(input("Введите шаг для значений x (Δx): "))
    return (a1, b1, a2, b2, a3, b3), x0, xk, dx  

def calculate_y_values(x_values, coefficients):
    """Вычисляет значения y для заданных x."""
    a1, b1, a2, b2, a3, b3 = coefficients
    return (
        a1 * np.sin(b1 * x_values) +
        a2 * np.sin(b2 * x_values) +
        a3 * np.sin(b3 * x_values)
    )

def display_table(x_values, y_values):
    """Отображает таблицу значений x и y."""
    print("\n=== Таблица значений x и y ===")
    print(f"{'x':^10} | {'y':^10}")
    print("-" * 23)
    for x, y in zip(x_values, y_values):
        print(f"{x:^10.4f} | {y:^10.4f}")

def plot_graph(x_values, y_values):
    """Строит график зависимости y от x."""
    plt.figure(figsize=(10, 6), facecolor='#f0f0f0')
    plt.plot(x_values, y_values, color='#ff5733', linestyle='--', marker='o', markersize=4)
    plt.title("График зависимости y(x)", fontsize=14, fontweight='bold')
    plt.xlabel("Значения x", fontsize=12, color='#333333')
    plt.ylabel("Значения y", fontsize=12, color='#333333')
    plt.grid(True, which='both', axis='both', color='#cccccc', linestyle='-.', linewidth=0.75)
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)
    plt.legend(['y(x)'], loc='upper right', fontsize=12)
    plt.tight_layout()
    plt.show()

def main():
    """Основная функция, выполняющая программу."""
    # Получение пользовательских входных данных
    coefficients, x0, xk, dx = get_user_input()

    # Создание массива значений x
    x_values = np.arange(x0, xk + dx, dx)
    
    # Расчет значений y
    y_values = calculate_y_values(x_values, coefficients)

    # Вывод таблицы значений
    display_table(x_values, y_values)

    # Построение графика
    plot_graph(x_values, y_values)

if __name__ == "__main__":
    main()
