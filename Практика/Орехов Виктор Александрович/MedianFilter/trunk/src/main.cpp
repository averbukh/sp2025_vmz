/**
 * @file main.cpp
 * @brief Демонстрация работы медианного фильтра на изображении буквы "О"
 * @author Орехов Виктор
 * @version 1.0
 */

#include <QApplication>
#include <QWidget>
#include <QGridLayout>
#include <QPushButton>
#include <QLabel>
#include <vector>
#include <algorithm>

/**
 * @class ImageGrid
 * @brief Виджет для отображения и обработки изображения с медианным фильтром
 *
 * Класс предоставляет функциональность для отображения пиксельного изображения
 * буквы "О" и применения к нему медианного фильтра размером 3x3.
 */
class ImageGrid : public QWidget {
    Q_OBJECT

private:
    QGridLayout* gridLayout;                         ///< Layout для размещения пикселей и кнопки
    std::vector<std::vector<int>> originalPixels;    ///< Исходное изображение буквы "О"
    std::vector<std::vector<int>> currentPixels;     ///< Текущее отображаемое изображение
    const int gridSize = 16;                         ///< Размер сетки (16x16 пикселей)
    const int cellSize = 20;                         ///< Размер одного пикселя в точках

public:
    /**
     * @brief Конструктор класса ImageGrid
     * @param parent Родительский виджет
     */
    ImageGrid(QWidget* parent = nullptr) : QWidget(parent) {
        gridLayout = new QGridLayout(this);
        gridLayout->setSpacing(1);

        initializeImage();
        displayImage();

        QPushButton* filterButton = new QPushButton("Применить медианный фильтр", this);
        gridLayout->addWidget(filterButton, gridSize, 0, 1, gridSize);

        connect(filterButton, &QPushButton::clicked, this, &ImageGrid::applyMedianFilter);
    }

private:
    /**
     * @brief Инициализирует изображение буквы "О"
     *
     * Создает бинарное изображение буквы "О" на черном фоне.
     * Белые пиксели (значение 1) формируют букву, черные (0) - фон.
     */
    void initializeImage() {
        // Инициализация пустого изображения (все черные пиксели)
        originalPixels = std::vector<std::vector<int>>(gridSize,
                          std::vector<int>(gridSize, 0));

        // Рисуем букву "О"
        // Внешний контур
        for (int i = 2; i <= 13; i++) {
            originalPixels[2][i] = 1;
            originalPixels[13][i] = 1;
        }
        for (int i = 3; i <= 12; i++) {
            originalPixels[i][2] = 1;
            originalPixels[i][13] = 1;
        }

        // Внутренний контур
        for (int i = 5; i <= 10; i++) {
            originalPixels[5][i] = 0;
            originalPixels[10][i] = 0;
        }
        for (int i = 6; i <= 9; i++) {
            originalPixels[i][5] = 0;
            originalPixels[i][10] = 0;
        }

        // Заполняем внутренность буквы белым
        for (int i = 3; i <= 12; i++) {
            for (int j = 3; j <= 12; j++) {
                originalPixels[i][j] = 1;
            }
        }

        // Вырезаем внутреннее отверстие
        for (int i = 6; i <= 9; i++) {
            for (int j = 6; j <= 9; j++) {
                originalPixels[i][j] = 0;
            }
        }

        currentPixels = originalPixels;
    }

    /**
     * @brief Отображает текущее изображение в виде сетки пикселей
     *
     * Создает QLabel для каждого пикселя, устанавливая соответствующий цвет
     * и добавляя их в gridLayout.
     */
    void displayImage() {
        // Очищаем старые label'ы
        QLayoutItem* item;
        while ((item = gridLayout->takeAt(0)) != nullptr) {
            delete item->widget();
            delete item;
        }

        // Создаем новые label'ы с пикселями
        for (int i = 0; i < gridSize; i++) {
            for (int j = 0; j < gridSize; j++) {
                QLabel* label = new QLabel(this);
                label->setFixedSize(cellSize, cellSize);

                if (currentPixels[i][j] == 1) {
                    label->setStyleSheet("background-color: white; border: 1px solid gray;");
                } else {
                    label->setStyleSheet("background-color: black; border: 1px solid gray;");
                }

                gridLayout->addWidget(label, i, j);
            }
        }

        // Добавляем кнопку обратно
        QPushButton* filterButton = new QPushButton("Применить медианный фильтр", this);
        gridLayout->addWidget(filterButton, gridSize, 0, 1, gridSize);
        connect(filterButton, &QPushButton::clicked, this, &ImageGrid::applyMedianFilter);
    }

    /**
     * @brief Применяет медианный фильтр размером 3x3 к текущему изображению
     *
     * Для каждого пикселя изображения рассматривается окно 3x3 вокруг него.
     * Значения всех пикселей в окне сортируются, и центральный пиксель
     * заменяется на медиану этих значений.
     *
     * @note Для пикселей на границах изображения несуществующие соседи
     *       считаются черными (значение 0).
     */
    void applyMedianFilter() {
        std::vector<std::vector<int>> filteredPixels = currentPixels;

        for (int i = 0; i < gridSize; i++) {
            for (int j = 0; j < gridSize; j++) {
                std::vector<int> neighbors;

                // Собираем соседей в окне 3x3
                for (int di = -1; di <= 1; di++) {
                    for (int dj = -1; dj <= 1; dj++) {
                        int ni = i + di;
                        int nj = j + dj;

                        // Если сосед внутри изображения, берем его значение
                        // Если снаружи - считаем черным (0)
                        if (ni >= 0 && ni < gridSize && nj >= 0 && nj < gridSize) {
                            neighbors.push_back(currentPixels[ni][nj]);
                        } else {
                            neighbors.push_back(0);
                        }
                    }
                }

                // Сортируем и находим медиану
                std::sort(neighbors.begin(), neighbors.end());
                filteredPixels[i][j] = neighbors[4]; // 4-й элемент - медиана для 9 элементов
            }
        }

        currentPixels = filteredPixels;
        displayImage();
    }

public slots:
    /**
     * @brief Сбрасывает изображение к исходному состоянию
     *
     * Восстанавливает исходное изображение буквы "О" без применения фильтра.
     */
    void resetImage() {
        currentPixels = originalPixels;
        displayImage();
    }
};

#include "main.moc"

/**
 * @brief Точка входа в приложение
 * @param argc Количество аргументов командной строки
 * @param argv Массив аргументов командной строки
 * @return Код возврата приложения
 *
 * Создает и запускает Qt приложение с виджетом ImageGrid.
 */
int main(int argc, char* argv[]) {
    QApplication app(argc, argv);

    ImageGrid window;
    window.setWindowTitle("Медианный фильтр - Буква О");
    window.setFixedSize(400, 400);
    window.show();

    return app.exec();
}
