import math
import matplotlib.pyplot as plt
from PIL import Image
import os

#Ввод параметров
print("Введите параметры функции y(x) = a1*sin(b1*x) + a2*sin(b2*x) + a3*sin(b3*x):")
a1 = float(input("a1 = "))
b1 = float(input("b1 = "))
a2 = float(input("a2 = "))
b2 = float(input("b2 = "))
a3 = float(input("a3 = "))
b3 = float(input("b3 = "))

x0 = float(input("x0 (начальное значение x) = "))
xk = float(input("xk (конечное значение x) = "))
dx = float(input("Δx (шаг) = "))

#Проверка шага
if dx <= 0:
    raise ValueError("Шаг Δx должен быть положительным числом!")

#Расчет таблицы
x_vals = []
y_vals = []

x = x0
while x <= xk + dx / 2:  # +dx/2 чтобы не потерять последнюю точку из-за округления
    y = a1 * math.sin(b1 * x) + a2 * math.sin(b2 * x) + a3 * math.sin(b3 * x)
    x_vals.append(x)
    y_vals.append(y)
    x += dx

#Вывод таблицы
print("\nТаблица значений функции:")
print("    x\t\t    y")
print("-" * 30)
for xi, yi in zip(x_vals, y_vals):
    print(f"{xi:10.4f}\t{yi:10.4f}")

#Построение графика и сохранение в выбранном формате
plt.figure(figsize=(8, 5))
plt.plot(x_vals, y_vals, 'b-', linewidth=2, label='y(x)')
plt.title("График функции y(x) = a1*sin(b1*x) + a2*sin(b2*x) + a3*sin(b3*x)")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.legend()

flag = True
print("Выберите формат сохранения графика:\n1 - .bmp (растровый формат)\n2 - .svg (векторный формат)")
choice = 0
while flag:
  choice = int(input("Выберите формат: "))
  if choice != 1 and choice != 2:
    print("Введите 1 или 2.")
    continue
  else:
    flag = False

if choice == 1:
  ftype = "bmp"
else:
  ftype = "svg"

filename = f"graph."

if ftype == "svg":
  plt.savefig(f"{filename}{ftype}", format=f"{ftype}", dpi=120, bbox_inches='tight')
  plt.close()
elif ftype == "bmp":
  ftype = "png"
  plt.savefig(f"{filename}{ftype}", format=f"{ftype}", dpi=120, bbox_inches='tight')
  plt.close()
  img = Image.open(f"{filename}{ftype}")
  ftype = "bmp"
  img.save(f"{filename}{ftype}", 'BMP')
  os.remove(f"{filename}png")

print(f"График успешно сохранен в файл: {os.curdir}\\{filename}{ftype}")
print("Готово!")