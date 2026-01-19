import numpy
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from math import sqrt

def getFilter(image, imageArray, w, d):
  # Параметры изображения
  width, height = image.size
  # Массив значений x и y
  xArr = []
  yArr = []
  # Количество итераций
  count = (width - w) // (d + 1)
  for i in range(count):
    left = i * d
    right = left + w

    # Проверяем выход за границы текущего положения фильтра
    if right > width:
      break
    # Воспользуемся срезами *синтаксис [start:stop:step]*
    # для получения текущего положения фильтра
    filter = imageArray[:, left:right]
    # Получаем размер половины среза фильтра
    halfWidth = w // 2

    leftHalf = filter[:, :halfWidth]
    rightHalf = filter[:, halfWidth:]

    # Подсчитаем сумму яркости элементов левой и правой половин
    sumLeft = int(np.sum(leftHalf))
    sumRight = int(np.sum(rightHalf))

    y = sumRight - sumLeft

    x = left + w / 2
    xArr.append(x)
    yArr.append(y)
  return xArr, yArr

def getTable(x, y):
  # Создаем таблицу с результатами
  df = pd.DataFrame({
      'x': x,
      'y(x)': y
  })

  print("Таблица значений x и y(x):")
  # Показываем первые 10 строк
  print(df.head(10))
  if len(df) > 10:
      print("...")
      # Показываем последние 10 строк
      print(df.tail(10))
  return

def getPlot(imagePath, x, y, w, d):
  # Устанавливаем отображаемую область для графиков
  table, (img1, img2) = plt.subplots(2, 1, figsize=(14, 10))

  # Отображение исходного изображения
  img = Image.open(imagePath)
  img1.imshow(img, cmap='gray')
  img1.set_title('Исходное изображение')
  img1.axis('off')

  # Построение графика y(x)
  img2.plot(x, y, 'b-', linewidth=2, label='y(x) = μ1(x)', zorder=3)

  # Ось X
  img2.axhline(y=0, color='black', linewidth=2, linestyle='-', label='Ось X', zorder=2)

  # ось Y
  if np.min(x) <= 0 <= np.max(x):
      img2.axvline(x=0, color='black', linewidth=1, linestyle='--', alpha=0.7, label='x=0')


  img2.set_xlabel('Координата x (пиксели)')
  img2.set_ylabel('y(x) = разница яркостей')
  img2.set_title(f'График функции y(x) = μ1(x)\n(w={w}, d={d})')
  img2.grid(True, alpha=0.3)
  img2.legend()

  # Устанавливаем одинаковые отступы по осям для симметрии
  y_max = max(np.max(y), -np.min(y))
  img2.set_ylim(-y_max * 1.1, y_max * 1.1)

  plt.tight_layout()
  plt.show()
  return

if __name__ == "__main__":
  # Получаем путь изображения
  imagePath = "04.png"
  imagePath2 = "09.png"
  # Получаем изображение
  image = Image.open(imagePath)
  image2 = Image.open(imagePath2)
  # Конвертируем в формат L (оттенки серого), так как нам необходима только яркость пикселей
  image = image.convert("L")
  image2 = image2.convert("L")
  # Переводим получившееся изображение в массив значений
  imageArray = np.array(image)
  imageArray2 = np.array(image2)
  # Переменная для использования программы
  choice = "y"
  while choice != "n":
    # Задаем ширину фильтра (кратно 4) и шаг
    w = 1
    d = 0
    while w % 4 != 0:
      try:
        w = int(input("Введите ширину фильтра (число кратное 4): "))
        if w % 4 != 0:
          print("Число должно быть кратно 4!")
          w = 1
      except:
        print("Введено некорректное значение.")
        w = 1
    while d < 1:
      try:
        d = int(input("Введите шаг (целое число больше 0): "))
        if d < 1:
          print("Число должно быть больше 0!")
          d = 0
      except:
        print("Введено некорректное значение.")
        d = 0
    # Вызываем функцию для решения задачи для первой картинки
    x, y = getFilter(image, imageArray, w, d)
    # Вызываем функцию для построения таблицы значений для первой картинки
    getTable(x, y)
    # Вызываем функцию для вывода графика для первой картинки
    getPlot(imagePath, x, y, w, d)

    # Вызываем функции для второй картинки
    x, y = getFilter(image2, imageArray2, w, d)
    getTable(x, y)
    getPlot(imagePath2, x, y, w, d)
    try:
      choice = input("Вы хотите ввести новые данные (y/n)? - ")
      if choice != "y" and choice != "n":
        print("Некорректный ввод. Программа будет завершена.")
        choice = "n"
    except:
        print("Некорректный ввод. Программа будет завершена.")
        choice = "n"
  print("\n\nПрограмма завершена.")


  #getSumBright(image, w,d)
  # Получаем значение RGB пикселя
  #pixelRGB = image.getpixel((X,Y))
  # Отдельно помещаем в каждую переменную значения параметров RGB
  #R,G,B = pixelRGB
  # Вычисляем яркость пикселя
  #brightness = sum([R,G,B])/3
  #print(brightness)