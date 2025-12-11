import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from PIL import Image

class ImageFilterAnalyzer:
    def __init__(self):
        print("=" * 60)
        print("АНАЛИЗ ИЗОБРАЖЕНИЙ - ФИЛЬТР АКТИВНОГО ВОСПРИЯТИЯ")
        print("=" * 60)
        
        # Получаем путь к директории программы
        self.program_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        print("Директория программы:", self.program_dir)
        
    def find_images_in_directory(self):
        """Поиск всех изображений в директории программы"""
        images = []
        
        # Проверяем все файлы в директории программы
        for file in os.listdir(self.program_dir):
            file_lower = file.lower()
            # Проверяем расширения файлов
            if (file_lower.endswith('.png') or 
                file_lower.endswith('.jpg') or 
                file_lower.endswith('.jpeg')):
                
                full_path = os.path.join(self.program_dir, file)
                # Проверяем, что это файл (а не папка)
                if os.path.isfile(full_path):
                    # Получаем размер файла
                    file_size = os.path.getsize(full_path)
                    images.append({
                        'name': file,
                        'path': full_path,
                        'size_kb': file_size / 1024
                    })
        
        return images
    
    def display_image_list(self, images):
        """Отображение списка найденных изображений"""
        if not images:
            print("\nВ директории программы не найдено изображений!")
            print("Доступные форматы: PNG, JPG, JPEG")
            print("\nТекущая директория:", self.program_dir)
            return False
        
        print(f"\nНайдено {len(images)} изображений в директории программы:")
        print("-" * 50)
        print("Номер  Имя файла")
        print("-" * 50)
        
        for i, img in enumerate(images, 1):
            print(f"{i:3}.   {img['name']}")
        
        print("-" * 50)
        return True
    
    def load_image(self):
        """Загрузка изображения"""
        print("\n" + "=" * 40)
        print("ЗАГРУЗКА ИЗОБРАЖЕНИЯ")
        print("=" * 40)
        
        while True:
            # Ищем все изображения в директории
            images = self.find_images_in_directory()
            
            # Показываем список
            if not self.display_image_list(images):
                print("\nВозможные решения:")
                print("1. Поместите изображения в ту же папку, что и программа")
                print("2. Используйте абсолютный путь к файлу")
                
                choice = input("\nВыберите действие (1-2): ").strip()
                
                if choice == '1':
                    print("\nТекущая директория:", self.program_dir)
                    input("Поместите изображения в эту папку и нажмите Enter...")
                    continue
                elif choice == '2':
                    return self.load_by_path()
                else:
                    continue
            
            # Если изображения найдены
            print("\nВарианты загрузки:")
            print("1. Выбрать из списка")
            print("2. Ввести путь вручную")
            print("3. Обновить список")
            
            try:
                choice = input("\nВыберите вариант (1-3): ").strip()
                
                if choice == '1':
                    # Выбор из списка
                    img_num = int(input(f"Введите номер изображения (1-{len(images)}): "))
                    if 1 <= img_num <= len(images):
                        return self._open_image(images[img_num-1]['path'])
                    else:
                        print("Неверный номер!")
                        continue
                        
                elif choice == '2':
                    # Ручной ввод пути
                    return self.load_by_path()
                    
                elif choice == '3':
                    # Обновить список
                    continue
                    
                else:
                    print("Неверный выбор!")
                    continue
                    
            except ValueError:
                print("Пожалуйста, введите число!")
            except Exception as e:
                print(f"Ошибка: {e}")
    
    def load_by_path(self):
        """Загрузка по указанному пути"""
        while True:
            print("\nВведите путь к изображению:")
            print("Примеры:")
            print("  image.png")
            print("  C:\\Users\\Name\\Desktop\\image.jpg")
            print("  ../folder/image.jpeg")
            
            path = input("\nПуть: ").strip()
            
            # Если путь относительный, делаем его абсолютным относительно директории программы
            if not os.path.isabs(path):
                path = os.path.join(self.program_dir, path)
            
            # Проверяем существование файла
            if not os.path.exists(path):
                print(f"Файл не найден: {path}")
                print(f"Текущая директория: {self.program_dir}")
                
                retry = input("Попробовать снова? (да/нет): ").lower()
                if retry in ['да', 'д', 'yes', 'y']:
                    continue
                else:
                    return None
            else:
                return self._open_image(path)
    
    def _open_image(self, path):
        """Открытие изображения"""
        try:
            print(f"\nПопытка открыть: {path}")
            
            # Проверяем, что это файл
            if not os.path.isfile(path):
                print("Это не файл!")
                return None
            
            # Проверяем размер файла
            file_size = os.path.getsize(path)
            if file_size == 0:
                print("Файл пустой!")
                return None
            
            print(f"Размер файла: {file_size / 1024:.1f} КБ")
            
            # Открываем изображение
            img = Image.open(path)
            
            # Получаем информацию об изображении
            print(f"Формат: {img.format}")
            print(f"Размер: {img.width}x{img.height} пикселей")
            print(f"Цветовой режим: {img.mode}")
            
            # Преобразуем в черно-белое
            if img.mode != 'L':
                print("Преобразование в черно-белое...")
                gray_img = img.convert('L')
            else:
                gray_img = img
            
            # Конвертируем в numpy массив
            img_array = np.array(gray_img)
            
            print("Изображение успешно загружено!")
            
            return {
                'array': img_array,
                'original': img,
                'gray': gray_img,
                'path': path,
                'filename': os.path.basename(path),
                'width': img.width,
                'height': img.height,
                'name': os.path.splitext(os.path.basename(path))[0]
            }
            
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            print("Проверьте:")
            print("1. Файл не поврежден")
            print("2. Это действительно изображение")
            print("3. Формат поддерживается (PNG, JPG, JPEG)")
            return None
    
    def get_parameters(self, image_width):
        """Получение параметров от пользователя"""
        print("\n" + "=" * 40)
        print("НАСТРОЙКА ПАРАМЕТРОВ ФИЛЬТРА")
        print("=" * 40)
        
        while True:
            try:
                print(f"\nШирина изображения: {image_width} пикселей")
                
                # Ширина фильтра
                w = int(input("Ширина фильтра w (должна быть кратна 4): "))
                
                if w <= 0:
                    print("Ширина должна быть положительной!")
                    continue
                
                if w % 4 != 0:
                    print(f"{w} не кратно 4!")
                    print(f"   Рекомендуемые значения: {w - (w % 4)} или {w + (4 - w % 4)}")
                    continue
                
                if w > image_width:
                    print(f"Ширина фильтра ({w}) больше ширины изображения ({image_width})!")
                    continue
                
                # Шаг фильтра
                max_d = min(100, image_width - w)
                d = int(input(f"Шаг фильтра d (1-{max_d}): "))
                
                if d <= 0 or d > max_d:
                    print(f"Шаг должен быть от 1 до {max_d}!")
                    continue
                
                print(f"\nПараметры установлены:")
                print(f"   Ширина фильтра: w = {w}")
                print(f"   Шаг фильтра: d = {d}")
                
                return w, d
                
            except ValueError:
                print("Пожалуйста, введите число!")
            except Exception as e:
                print(f"Ошибка: {e}")
    
    def apply_filter(self, image_data, w, d):
        """Применение фильтра активного восприятия"""
        print(f"\nПрименение фильтра...")
        
        img_array = image_data['array']
        width = image_data['width']
        height = image_data['height']
        
        x_values = []
        y_values = []
        total_steps = (width - w) // d + 1
        
        print(f"Всего позиций для анализа: {total_steps}")
        
        for i, start_x in enumerate(range(0, width - w + 1, d)):
            # Простой прогресс-бар
            if i % max(1, total_steps // 10) == 0:
                progress = (i + 1) / total_steps * 100
                print(f"  Прогресс: {progress:.0f}%", end='\r')
            
            # Центр текущего окна
            center_x = start_x + w / 2
            
            # Вырезаем область
            region = img_array[0:height, start_x:start_x + w]
            
            # Делим на левую и правую половины
            half_w = w // 2
            left_half = region[:, 0:half_w]
            right_half = region[:, half_w:]
            
            # Считаем сумму яркости
            left_sum = np.sum(left_half)
            right_sum = np.sum(right_half)
            
            # Разность сумм
            diff = right_sum - left_sum
            
            x_values.append(center_x)
            y_values.append(diff)
        
        print("  Прогресс: 100%")
        
        x = np.array(x_values)
        y = np.array(y_values)
        
        print(f"Обработано точек: {len(x)}")
        return x, y
    
    def find_boundaries(self, y):
        """Автоматический поиск границ символов"""
        threshold = 0.3  # Фиксированный порог по умолчанию
        peaks = []
        valleys = []
        
        for i in range(1, len(y) - 1):
            # Ищем локальные максимумы (границы символов)
            if y[i] > y[i-1] and y[i] > y[i+1]:
                if y[i] > np.max(y) * threshold:
                    peaks.append(i)
            
            # Ищем локальные минимумы
            if y[i] < y[i-1] and y[i] < y[i+1]:
                if y[i] < np.min(y) * threshold:
                    valleys.append(i)
        
        return np.array(peaks), np.array(valleys), threshold
    
    def display_table(self, x, y, peaks, valleys):
        """Отображение таблицы значений x, y"""
        print("\n" + "=" * 60)
        print("ТАБЛИЦА ЗНАЧЕНИЙ y(x)")
        print("=" * 60)
        
        print(f"\nВсего точек: {len(x)}")
        
        # Определяем сколько строк показывать (первые 20)
        show_rows = min(20, len(x))
        
        print(f"\nПервые {show_rows} значений:")
        print("-" * 50)
        print(f"{'№':>4} {'X':>10} {'Y':>12} {'Граница':>10} {'Минимум':>10}")
        print("-" * 50)
        
        for i in range(show_rows):
            is_boundary = "ДА" if i in peaks else ""
            is_valley = "ДА" if i in valleys else ""
            print(f"{i+1:4d} {x[i]:10.1f} {y[i]:12.0f} {is_boundary:>10} {is_valley:>10}")
        
        if len(x) > show_rows:
            print(f"... и еще {len(x) - show_rows} строк")
        
        print("-" * 50)
        
        # Статистика
        print(f"\nСтатистика значений y:")
        print(f"  Минимальное значение: {np.min(y):.0f}")
        print(f"  Максимальное значение: {np.max(y):.0f}")
        print(f"  Среднее значение: {np.mean(y):.0f}")
        print(f"  Стандартное отклонение: {np.std(y):.0f}")
        
        # Результаты поиска границ
        print(f"\nРезультаты поиска границ (порог: 0.3):")
        print(f"  Найдено границ символов: {len(peaks)}")
        print(f"  Найдено минимумов: {len(valleys)}")
        
        if len(peaks) > 0:
            print(f"\nКоординаты границ (X):")
            for i, peak_idx in enumerate(peaks[:10], 1):
                if peak_idx < len(x):
                    print(f"  Граница {i}: x = {x[peak_idx]:.1f} пикселей")
            
            if len(peaks) > 10:
                print(f"  ... и еще {len(peaks) - 10} границ")
    
    def plot_function(self, x, y, image_data, w, d, peaks, valleys):
        """Построение графика функции y(x)"""
        plt.figure(figsize=(14, 8))
        
        # График функции y(x)
        plt.plot(x, y, 'b-', linewidth=2, label=f'y(x), w={w}, d={d}')
        plt.xlabel('Координата X (центр фильтра, пиксели)', fontsize=12)
        plt.ylabel('Разность яркостей Y', fontsize=12)
        plt.title(f'График функции y(x) = μ₁(x)\nИзображение: {image_data["filename"]}', fontsize=14)
        
        # Отмечаем границы на графике
        if len(peaks) > 0:
            plt.plot(x[peaks], y[peaks], 'ro', markersize=6, label=f'Границы символов ({len(peaks)})')
            for peak in peaks:
                plt.axvline(x=x[peak], color='red', linestyle='--', alpha=0.5)
        
        # Отмечаем минимумы на графике
        if len(valleys) > 0:
            plt.plot(x[valleys], y[valleys], 'go', markersize=6, label=f'Минимумы ({len(valleys)})')
        
        # Настройки сетки
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Добавляем легенду
        plt.legend(fontsize=12)
        
        # Настройка осей
        plt.tight_layout()
        
        # Сохранение графика
        filename = f"график_{image_data['name']}_w{w}_d{d}.png"
        save_path = os.path.join(self.program_dir, filename)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"\nГрафик сохранен: {save_path}")
        
        plt.show()
    
    def save_results(self, image_data, x, y, w, d, peaks, valleys, threshold):
        """Сохранение результатов в текстовый файл"""
        filename = f"результаты_{image_data['name']}_w{w}_d{d}.txt"
        save_path = os.path.join(self.program_dir, filename)
        
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("РЕЗУЛЬТАТЫ АНАЛИЗА ИЗОБРАЖЕНИЯ С ФИЛЬТРОМ АКТИВНОГО ВОСПРИЯТИЯ\n")
                f.write("=" * 70 + "\n\n")
                
                f.write(f"Исходный файл: {image_data['filename']}\n")
                f.write(f"Размер изображения: {image_data['width']}x{image_data['height']} пикселей\n")
                f.write(f"Параметры фильтра: w={w}, d={d}\n")
                f.write(f"Порог для поиска границ: {threshold}\n\n")
                
                f.write(f"Всего точек анализа: {len(x)}\n")
                f.write(f"Найдено границ символов: {len(peaks)}\n")
                f.write(f"Найдено минимумов: {len(valleys)}\n\n")
                
                f.write("СТАТИСТИКА ЗНАЧЕНИЙ Y:\n")
                f.write("-" * 50 + "\n")
                f.write(f"Минимальное значение: {np.min(y):.0f}\n")
                f.write(f"Максимальное значение: {np.max(y):.0f}\n")
                f.write(f"Среднее значение: {np.mean(y):.0f}\n")
                f.write(f"Стандартное отклонение: {np.std(y):.0f}\n\n")
                
                if len(peaks) > 0:
                    f.write("КООРДИНАТЫ ОБНАРУЖЕННЫХ ГРАНИЦ СИМВОЛОВ:\n")
                    f.write("-" * 50 + "\n")
                    for i, peak_idx in enumerate(peaks, 1):
                        if peak_idx < len(x):
                            f.write(f"Граница {i:3d}: X = {x[peak_idx]:8.1f} пикселей, Y = {y[peak_idx]:12.0f}\n")
                    f.write("\n")
                
                f.write("ПОЛНАЯ ТАБЛИЦА ЗНАЧЕНИЙ:\n")
                f.write("-" * 70 + "\n")
                f.write(f"{'№':>5} {'X':>12} {'Y':>15} {'Граница':>10} {'Минимум':>10}\n")
                f.write("-" * 70 + "\n")
                
                for i in range(len(x)):
                    is_boundary = "ДА" if i in peaks else ""
                    is_valley = "ДА" if i in valleys else ""
                    f.write(f"{i+1:5d} {x[i]:12.1f} {y[i]:15.0f} {is_boundary:>10} {is_valley:>10}\n")
            
            print(f"Результаты сохранены: {save_path}")
            
            # Также сохраняем упрощенный CSV файл
            csv_filename = f"данные_{image_data['name']}_w{w}_d{d}.csv"
            csv_path = os.path.join(self.program_dir, csv_filename)
            
            with open(csv_path, 'w', encoding='utf-8') as f:
                f.write("Номер,X,Y,Граница_символа,Минимум\n")
                for i in range(len(x)):
                    is_boundary = "1" if i in peaks else "0"
                    is_valley = "1" if i in valleys else "0"
                    f.write(f"{i+1},{x[i]:.1f},{y[i]:.0f},{is_boundary},{is_valley}\n")
            
            print(f"Данные в CSV формате сохранены: {csv_path}")
            
        except Exception as e:
            print(f"Ошибка сохранения результатов: {e}")
    
    def run(self):
        """Основной цикл программы"""
        print("\nИНСТРУКЦИЯ:")
        print("1. Поместите PNG/JPG изображения в папку с программой")
        print("2. Выберите изображение для анализа")
        print("3. Укажите параметры фильтра (w и d)")
        print("4. Получите график функции y(x) и таблицу значений\n")
        
        while True:
            # Загрузка изображения
            image_data = self.load_image()
            if image_data is None:
                print("Не удалось загрузить изображение.")
                retry = input("Попробовать снова? (да/нет): ").lower()
                if retry not in ['да', 'д', 'yes', 'y']:
                    break
                continue
            
            # Ввод параметров
            w, d = self.get_parameters(image_data['width'])
            
            # Применение фильтра
            x, y = self.apply_filter(image_data, w, d)
            
            # Автоматический поиск границ (с фиксированным порогом 0.3)
            peaks, valleys, threshold = self.find_boundaries(y)
            
            # Отображение таблицы
            self.display_table(x, y, peaks, valleys)
            
            # Построение графика
            self.plot_function(x, y, image_data, w, d, peaks, valleys)
            
            # Сохранение результатов
            self.save_results(image_data, x, y, w, d, peaks, valleys, threshold)
            
            # Повторный анализ
            while True:
                choice = input("\nХотите проанализировать другое изображение? (да/нет): ").lower().strip()
                if choice in ['да', 'д', 'yes', 'y']:
                    break
                elif choice in ['нет', 'н', 'no', 'n']:
                    print("\nСпасибо за использование программы!")
                    return
                else:
                    print("Пожалуйста, введите 'да' или 'нет'")


def main():
    """Главная функция"""
    print("=" * 70)
    print("ПРОГРАММА АНАЛИЗА ИЗОБРАЖЕНИЙ С ФИЛЬТРОМ АКТИВНОГО ВОСПРИЯТИЯ")
    print("=" * 70)
    print("Для каждого изображения строится график функции y(x) = μ₁(x)")
    print("где y - разность яркостей правой и левой половин фильтра")
    print("x - координата центра фильтра по горизонтали")
    print("Автоматический поиск границ символов выполняется с порогом 0.3")
    print("=" * 70)
    
    try:
        # Проверяем необходимые библиотеки
        import numpy as np
        import matplotlib.pyplot as plt
        from PIL import Image
        
        print("Все библиотеки загружены успешно!")
        
        # Запускаем анализатор
        analyzer = ImageFilterAnalyzer()
        analyzer.run()
        
    except ImportError as e:
        print(f"Ошибка: {e}")
        print("\nДля установки необходимых библиотек выполните команды:")
        print("pip install numpy matplotlib pillow")


if __name__ == "__main__":
    main()