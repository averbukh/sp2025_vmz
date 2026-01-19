from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror, showinfo

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image as ImagePIL
from tkinter import *
from tkinter import ttk

fileName = ""

def getFilter(ev = None):
  # Изображение
  if (fileName == ""):
      showerror("Ошибка!", "Файл не выбран.")
      return
  image = ImagePIL.open(fileName)
  image = image.convert("L")
  imageArray = np.array(image)
  w = int(inpW.get("1.0", END))
  if w % 4 != 0:
      showerror("Ошибка!", "Ширина фильтра должна быть кратна 4!")
      return
  d = int(inpD.get("1.0", END))
  if d < 1:
      showerror("Ошибка!", "Шаг должен быть больше 0!")
      return

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
  getTable(xArr, yArr, ev)

def getTable(x, y, ev = None):
  # Создаем таблицу с результатами
  df = pd.DataFrame({
      'x': x,
      'y(x)': y
  })

  tree = ttk.Treeview(root, columns=list(df.columns), show="headings")
  for col in df.columns:
      tree.heading(col, text=col)
      tree.column(col, width=100)
  for index, row in df.iterrows():
      tree.insert('', 'end', values=list(row))
  tree.grid(row=0, column=5, rowspan=6, columnspan=2, pady=10, padx=10, sticky="news")
  getPlot(x, y, ev)

def getPlot(x, y, ev=None):
    try:
        plotFrame = Frame(root)
        plotFrame.grid(row=5, column=0,
                       columnspan=2,
                       pady=10, padx=10,
                       sticky="news")

        # Устанавливаем отображаемую область для графиков
        global fig
        fig = Figure(figsize=(6, 2), dpi=100)
        plotAx = fig.add_subplot(111)

        # Построение графика y(x)
        plotAx.plot(x, y, 'b-', linewidth=2, label='y(x) = μ1(x)', zorder=3)
        # Ось X
        plotAx.axhline(y=0, color='black', linewidth=2, linestyle='-', label='Ось X', zorder=2)
        # ось Y
        if np.min(x) <= 0 <= np.max(x):
            plotAx.axvline(x=0, color='black', linewidth=1, linestyle='--', alpha=0.7, label='x=0')

        plotAx.set_xlabel('Координата x (пиксели)')
        plotAx.set_ylabel('y(x) = разница яркостей')
        plotAx.set_title(f'График функции y(x) = μ1(x)')
        plotAx.grid(True, alpha=0.3)
        plotAx.legend()

        # Устанавливаем одинаковые отступы по осям для симметрии
        y_max = max(np.max(y), -np.min(y))
        plotAx.set_ylim(-y_max * 1.1, y_max * 1.1)
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=plotFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH,expand=1)
    except:
        showerror("Ошибка!", "Значение W слишком большое.")
    # Сохраняем SVG
    #filename = f"{w}_{d}_{imagePath}.svg"
    #plt.savefig(f"{filename}", format=f"svg", dpi=120, bbox_inches='tight')
    #plt.close()
    return

def getFile(ev = None):
  filepath = askopenfilename(title="Выберите файл",
                             filetypes=[("Pictures .png", "*.png")])
  if filepath != "":
      global fileName
      fileName = filepath
      filepath = filepath.split("/")
      filepath = filepath[len(filepath)-1]
      inpF.configure(state="normal")
      inpF.delete("1.0", END)
      inpF.insert("1.0", filepath)
      inpF.configure(state="disabled")

def savePlot(ev=None):
    filepath = asksaveasfilename(title="plotter",
                                 defaultextension=".png",
                                 filetypes=[("PNG files", "*.png"),
                                            ("SVG files", "*.svg"),
                                            ("PDF files", "*.pdf"),
                                            ("All files", "*.*")])
    if filepath:
        try:
            fig.savefig(filepath, dpi=300, bbox_inches='tight')
            showinfo("Информация", f"График сохранен как: {filepath}")
        except Exception as e:
            showerror("Ошибка!", f"Ошибка сохранения файла: {e}")

def getGUI():
  global root
  root = Tk()
  root.title("Lab. 2 | Skvortsov A.P.")
  root.geometry('820x520')
  root.resizable(width=False, height=False)

  # Поле для выбора файла
  labF = Label(root,
               text="Выбранный файл: ",
               width=15, height=1,
               font=("Times New Roman", 12))
  labF.grid(row=0, column=0,
            pady=10, padx=[5, 0],
            ipady=0, ipadx=0,
            sticky="w")
  global inpF
  inpF = Text(root,
              width=30, height=1,
              bg="lightgray",
              font=("Times New Roman", 12))
  inpF.configure(state="disabled")
  inpF.grid(row=0, column=1,
            pady=10, padx=[5, 10],
            sticky="w")
  butF = Button(root,
                text="Выбрать файл ",
                height=1,
                bg="gray95",
                activebackground="gray75",
                font=("Times New Roman", 12),
                command=getFile)
  butF.grid(row=1, column=0,
            columnspan=2,
            pady=10, padx=[5, 0],
            ipady=0, ipadx=0,
            sticky="news")

  # Текстовое поле для ввода ширины фильтра
  labW = Label(root,
               text = "Ширина фильтра (w)",
               width=15, height=1,
               font=("Times New Roman", 12))
  labW.grid(row=2, column=0,
            pady=10, padx=[10, 0],
            ipady=0, ipadx=0,
            sticky="w")
  global inpW
  inpW = Text(root,
              width=30, height=1,
              font=("Times New Roman", 12))
  inpW.grid(row=2, column=1,
            pady=10, padx=[5, 10],
            sticky="w")

  # Текстовое поле для ввода ширины фильтра
  labD = Label(root,
               text = "Шаг (d)",
               width=15, height=1,
               font=("Times New Roman", 12))
  labD.grid(row=3, column=0,
            pady=10, padx=[10, 0],
            ipady=0, ipadx=0,
            sticky="w")
  global inpD
  inpD = Text(root,
              width=30, height=1,
              font=("Times New Roman", 12))
  inpD.grid(row=3, column=1,
            pady=10, padx=[5, 10],
            sticky="w")

  # Кнопка рассчета
  btn = Button(root,
               text="Рассчитать",
               width=30, height=1,
               bg="gray95",
               activebackground="gray75",
               font=("Times New Roman", 12),
               command=getFilter)
  btn.grid(row=4, column=0,
           pady=10, padx=[5, 0],
           ipady=0, ipadx=0,
           sticky="news")
  # Кнопка сохранения файла
  btnSave = Button(root,
               text="Сохранить график",
               width=30, height=1,
               bg="gray95",
               activebackground="gray75",
               font=("Times New Roman", 12),
               command=savePlot)
  btnSave.grid(row=4,column=1,
           pady=10, padx=[5, 0],
           ipady=0, ipadx=0,
           sticky="news")

  root.mainloop()

  return

if __name__ == "__main__":
  # Вызов функции отрисовки GUI
  getGUI()
  quit()
