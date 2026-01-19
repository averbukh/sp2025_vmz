from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def getImage(filename):
   with Image.open(filename) as img:
      img.load()
   wImg, hImg = img.size
   print("Размерность изображения: ", wImg, 'на', hImg, 'пикселей')
   gimg = img.convert("L")
   return gimg, wImg, hImg

def getW():
   while True:
      wFlt = int(input('Введите ширину фильтра: '))
      if ((wFlt % 4 == 0) & (wFlt >= 4)):
         return wFlt
      print("Ширина должна быть кратна 4! Введите заново")

def getD():
   while True:
      dFlt = int(input('Введите шаг фильтра: '))
      if (dFlt >= 1):
         return dFlt
      print("Шаг должен быть целым числом большим либо равным 1!")

def filterMu1(gimg, wImg, wFlt, hImg, dFlt):
   imgArr = np.array(gimg)  
   xVal = []
   yVal = []
   curX = 0
   while (curX + wFlt <= wImg):
      midX = curX + wFlt // 2
      window = imgArr[0 : hImg , curX : curX + wFlt]
      wHalf = wFlt // 2
      wLeft = window[0:hImg, 0:wHalf].astype(np.int64)
      wRight = window[0:hImg, wHalf:wFlt].astype(np.int64)
      y = np.sum(wRight) - np.sum(wLeft)
      xVal.append(midX)
      yVal.append(y)
      curX += dFlt
   return xVal, yVal

def valTable(xVal, yVal):
   with open("output.txt", 'w') as file:
      print("\nТаблица y(x): ")
      file.write(f"Резльтаты работы программы: \n")
      for x, y in zip(xVal, yVal):
         file.write(f"{x}:\t|\t{y}\n")
         print(f"{x}:\t|\t{y}")

def plot(xVal, yVal):
   plt.figure(figsize=(12, 8), facecolor= "#eeeeee")
   plt.plot(xVal, yVal, color='green', marker='o',
      linestyle='dashed', linewidth=2, markersize=3)
   plt.title("График F(x)", fontsize=10, fontweight='bold')
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

def main():
   imgPath = input('Введите путь к изображению: ')
   if '\\' in imgPath:
      imgPath = fr"{imgPath}"
   gimg, wImg, hImg = getImage(imgPath)
   wFlt = getW()
   dFlt = getD()
   xVal, yVal = filterMu1(gimg, wImg, wFlt, hImg, dFlt)
   valTable(xVal, yVal)
   plot(xVal, yVal)

if __name__ == "__main__":
    main()