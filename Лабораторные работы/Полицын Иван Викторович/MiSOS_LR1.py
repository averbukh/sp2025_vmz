# numpy нужен для функций arrange() и sin()
import numpy as np
# matplotlib используется для построения самого графика
import matplotlib.pyplot as plt

# Ввод параметров
def parameters():
   a1 = float(input("a1: "))
   b1 = float(input("b1: "))
   a2 = float(input("a2: "))
   b2 = float(input("b2: "))
   a3 = float(input("a3: "))
   b3 = float(input("b3: "))
   xS = float(input("xS: "))
   xE = float(input("xE: "))
   xD = float(input("xD: "))
   xVal = np.arange(xS, xE + xD, xD)
   return a1, b1, a2, b2, a3, b3, xVal

# Вычисление y по x, отображение вычисляемых значений в терминал
def calculation(a1, b1, a2, b2, a3, b3, xVal):
   yVal = []
   print("Таблица значений F(x)")
   for x in xVal:
      y = (a1 * np.sin(b1 * x)) + (a2 * np.sin(b2 * x)) + (a3 * np.sin(b3 * x))
      yVal.append(y)
      print("x:", round(x, 3), "    y:", round(y, 3))
   return xVal, yVal

# Построение графика и его вывод при помощи matplotlib
def plot(xVal, yVal):
   plt.figure(figsize=(12, 8), facecolor="#eeeeee")
   plt.plot(xVal, yVal, color='green', marker='o',
      linestyle='dashed', linewidth=2, markersize=3)
   plt.title("График функции F(x)", fontsize=10, fontweight='bold')
   plt.xlabel("X", fontsize=10, color='#333333')
   plt.ylabel("Y", fontsize=10, color='#333333')
   plt.grid(True, which='both', axis='both', color='#cccccc', 
      linestyle='-', linewidth=0.75)
   plt.axhline(0, color='black', linewidth=1)
   plt.axvline(0, color='black', linewidth=1)
   plt.legend(['F(x)'], loc='upper right', fontsize=10)
   plt.tight_layout()
   plt.savefig('plot.svg')
   plt.show()

# Ввод, вычисление, построение
def main():
   parametrs = parameters()
   xVal, yVal = calculation(*parametrs)
   plot(xVal, yVal)
   print("Для завершения работы закройте окно графика.")

if __name__ == "__main__":
    main()

