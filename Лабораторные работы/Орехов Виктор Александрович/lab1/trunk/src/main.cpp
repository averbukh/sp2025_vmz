/**
 * @file main.cpp
 * @brief Основной файл приложения для построения графика функции
 * @details
 * Приложение для расчета и визуализации функции:
 * y(x) = a1 * sin(b1 * x) + a2 * sin(b2 * x) + a3 * sin(b3 * x)
 *
 * @author Орехов Виктор
 * @date 2025
 * @version 1.0
 */

#include <QApplication>
#include <QMainWindow>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QTableWidget>
#include <QLabel>
#include <QHeaderView>
#include <QMessageBox>
#include <QtMath>
#include <QGroupBox>
#include <QFrame>
#include <QFont>
#include <QScrollBar>

// Подключаем заголовочные файлы для Qt Charts
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>
#include <QtCharts/QValueAxis>

using namespace QtCharts;

/**
 * @brief Главное окно приложения
 *
 * Класс представляет основное окно приложения с элементами управления
 * для ввода параметров функции, отображения таблицы значений и графика.
 */
class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    /**
     * @brief Конструктор главного окна
     * @param parent Родительский виджет
     */
    explicit MainWindow(QWidget *parent = nullptr) : QMainWindow(parent)
    {
        setStyleSheet(loadStyleSheet());
        setupUI();
        connectSignals();
    }

private slots:
    /**
     * @brief Слот для расчета функции по введенным параметрам
     *
     * Выполняет валидацию введенных данных, расчет значений функции
     * и обновление таблицы и графика.
     */
    void calculateFunction()
    {
        // Получение значений от пользователя
        bool ok;
        double a1 = a1Edit->text().toDouble(&ok);
        if (!ok) { showError("Неверное значение a1"); return; }

        double b1 = b1Edit->text().toDouble(&ok);
        if (!ok) { showError("Неверное значение b1"); return; }

        double a2 = a2Edit->text().toDouble(&ok);
        if (!ok) { showError("Неверное значение a2"); return; }

        double b2 = b2Edit->text().toDouble(&ok);
        if (!ok) { showError("Неверное значение b2"); return; }

        double a3 = a3Edit->text().toDouble(&ok);
        if (!ok) { showError("Неверное значение a3"); return; }

        double b3 = b3Edit->text().toDouble(&ok);
        if (!ok) { showError("Неверное значение b3"); return; }

        double x0 = x0Edit->text().toDouble(&ok);
        if (!ok) { showError("Неверное значение x0"); return; }

        double xk = xkEdit->text().toDouble(&ok);
        if (!ok) { showError("Неверное значение xk"); return; }

        double dx = dxEdit->text().toDouble(&ok);
        if (!ok) { showError("Неверное значение Δx"); return; }

        if (dx <= 0) {
            showError("Шаг Δx должен быть положительным");
            return;
        }

        if (x0 >= xk) {
            showError("Начальное значение x0 должно быть меньше конечного xk");
            return;
        }

        // Расчет функции
        QVector<double> xValues, yValues;
        calculateYFunction(a1, b1, a2, b2, a3, b3, x0, xk, dx, xValues, yValues);

        // Обновление таблицы
        updateTable(xValues, yValues);

        // Обновление графика
        updateChart(xValues, yValues);
    }

    /**
     * @brief Слот для очистки всех полей ввода и результатов
     */
    void clearAll()
    {
        a1Edit->clear();
        b1Edit->clear();
        a2Edit->clear();
        b2Edit->clear();
        a3Edit->clear();
        b3Edit->clear();
        x0Edit->clear();
        xkEdit->clear();
        dxEdit->clear();
        tableWidget->setRowCount(0);

        // Очистка графика
        QChart *emptyChart = new QChart();
        emptyChart->setTitle("График функции y(x)");
        chartView->setChart(emptyChart);
    }

private:
    /**
     * @brief Загружает и возвращает таблицу стилей для приложения
     * @return QString Строка с CSS-стилями
     */
    QString loadStyleSheet()
    {
        return R"(
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #2c3e50, stop: 1 #34495e);
            }

            QGroupBox {
                font-weight: bold;
                font-size: 12px;
                color: #ecf0f1;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: rgba(52, 73, 94, 0.8);
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 8px;
                background-color: #3498db;
                color: white;
                border-radius: 4px;
            }

            QLabel {
                color: #ecf0f1;
                font-weight: bold;
                font-size: 11px;
            }

            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                font-size: 11px;
                background: #ecf0f1;
                selection-background-color: #3498db;
            }

            QLineEdit:focus {
                border-color: #3498db;
                background: white;
            }

            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #3498db, stop: 1 #2980b9);
                border: none;
                border-radius: 6px;
                color: white;
                font-weight: bold;
                font-size: 11px;
                padding: 10px;
                min-width: 80px;
            }

            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #3cb0fd, stop: 1 #3498db);
            }

            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #2980b9, stop: 1 #21618c);
            }

            QPushButton#calculateButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #27ae60, stop: 1 #229954);
            }

            QPushButton#calculateButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #2ecc71, stop: 1 #27ae60);
            }

            QPushButton#clearButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #e74c3c, stop: 1 #c0392b);
            }

            QPushButton#clearButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #ff6b6b, stop: 1 #e74c3c);
            }

            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #dee2e6;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                font-size: 10px;
            }

            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #dee2e6;
            }

            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }

            QHeaderView::section {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 8px;
                border: none;
            }

            QScrollBar:vertical {
                border: none;
                background: #ecf0f1;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background: #95a5a6;
                border-radius: 6px;
                min-height: 20px;
            }

            QScrollBar::handle:vertical:hover {
                background: #7f8c8d;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        )";
    }

    /**
     * @brief Настраивает пользовательский интерфейс
     *
     * Создает и размещает все элементы управления на форме,
     * настраивает компоновку и внешний вид.
     */
    void setupUI()
    {
        QWidget *centralWidget = new QWidget(this);
        centralWidget->setObjectName("centralWidget");
        setCentralWidget(centralWidget);

        QVBoxLayout *mainLayout = new QVBoxLayout(centralWidget);
        mainLayout->setSpacing(15);
        mainLayout->setContentsMargins(20, 20, 20, 20);

        // Заголовок
        QLabel *titleLabel = new QLabel("График функции: y(x) = a₁⋅sin(b₁⋅x) + a₂⋅sin(b₂⋅x) + a₃⋅sin(b₃⋅x)");
        titleLabel->setStyleSheet("font-size: 16px; font-weight: bold; color: #ecf0f1; padding: 10px;");
        titleLabel->setAlignment(Qt::AlignCenter);
        mainLayout->addWidget(titleLabel);

        // Группа параметров
        QGroupBox *paramsGroup = new QGroupBox("Параметры функции");
        QHBoxLayout *paramsLayout = new QHBoxLayout(paramsGroup);

        // Колонка 1 - Первое слагаемое
        QVBoxLayout *col1 = createParameterColumn("Первое слагаемое", a1Edit, b1Edit, "1.0", "1.0");

        // Колонка 2 - Второе слагаемое
        QVBoxLayout *col2 = createParameterColumn("Второе слагаемое", a2Edit, b2Edit, "0.5", "2.0");

        // Колонка 3 - Третье слагаемое
        QVBoxLayout *col3 = createParameterColumn("Третье слагаемое", a3Edit, b3Edit, "0.3", "3.0");

        // Колонка 4 - Диапазон
        QVBoxLayout *col4 = createRangeColumn();

        // Колонка 5 - Управление
        QVBoxLayout *col5 = createControlColumn();

        paramsLayout->addLayout(col1);
        paramsLayout->addLayout(col2);
        paramsLayout->addLayout(col3);
        paramsLayout->addLayout(col4);
        paramsLayout->addLayout(col5);

        mainLayout->addWidget(paramsGroup);

        // Таблица и график в горизонтальном layout
        QHBoxLayout *resultsLayout = new QHBoxLayout();
        resultsLayout->setSpacing(15);

        // Таблица
        QGroupBox *tableGroup = new QGroupBox("Таблица значений");
        QVBoxLayout *tableLayout = new QVBoxLayout(tableGroup);
        tableWidget = new QTableWidget();
        tableWidget->setColumnCount(2);
        tableWidget->setHorizontalHeaderLabels(QStringList() << "x" << "y(x)");
        tableWidget->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
        tableWidget->setAlternatingRowColors(true);
        tableWidget->setSelectionBehavior(QAbstractItemView::SelectRows);
        tableLayout->addWidget(tableWidget);

        // График
        QGroupBox *chartGroup = new QGroupBox("График функции");
        QVBoxLayout *chartLayout = new QVBoxLayout(chartGroup);
        chartView = new QChartView();
        chartView->setRenderHint(QPainter::Antialiasing);
        chartView->setStyleSheet("background: white; border-radius: 6px;");
        chartLayout->addWidget(chartView);

        resultsLayout->addWidget(tableGroup, 1);
        resultsLayout->addWidget(chartGroup, 2);

        mainLayout->addLayout(resultsLayout, 1);

        setWindowTitle("Function Plotter - Визуализация математических функций");
        setMinimumSize(1200, 800);
        resize(1400, 900);
    }

    /**
     * @brief Создает колонку параметров для одного слагаемого функции
     * @param title Заголовок колонки
     * @param aEdit Ссылка на указатель для поля ввода коэффициента a
     * @param bEdit Ссылка на указатель для поля ввода коэффициента b
     * @param aDefault Значение по умолчанию для коэффициента a
     * @param bDefault Значение по умолчанию для коэффициента b
     * @return QVBoxLayout* Вертикальный layout с элементами управления
     */
    QVBoxLayout* createParameterColumn(const QString& title, QLineEdit* &aEdit, QLineEdit* &bEdit,
                                      const QString& aDefault, const QString& bDefault)
    {
        QVBoxLayout *layout = new QVBoxLayout();

        QLabel *titleLabel = new QLabel(title);
        titleLabel->setAlignment(Qt::AlignCenter);
        titleLabel->setStyleSheet("font-weight: bold; color: #3498db; margin-bottom: 5px;");
        layout->addWidget(titleLabel);

        layout->addWidget(new QLabel("Коэффициент a:"));
        aEdit = new QLineEdit(aDefault);
        layout->addWidget(aEdit);

        layout->addWidget(new QLabel("Коэффициент b:"));
        bEdit = new QLineEdit(bDefault);
        layout->addWidget(bEdit);

        return layout;
    }

    /**
     * @brief Создает колонку для ввода диапазона вычислений
     * @return QVBoxLayout* Вертикальный layout с элементами управления диапазоном
     */
    QVBoxLayout* createRangeColumn()
    {
        QVBoxLayout *layout = new QVBoxLayout();

        QLabel *titleLabel = new QLabel("Диапазон вычислений");
        titleLabel->setAlignment(Qt::AlignCenter);
        titleLabel->setStyleSheet("font-weight: bold; color: #3498db; margin-bottom: 5px;");
        layout->addWidget(titleLabel);

        layout->addWidget(new QLabel("Начало x₀:"));
        x0Edit = new QLineEdit("0.0");
        layout->addWidget(x0Edit);

        layout->addWidget(new QLabel("Конец xₖ:"));
        xkEdit = new QLineEdit("10.0");
        layout->addWidget(xkEdit);

        layout->addWidget(new QLabel("Шаг Δx:"));
        dxEdit = new QLineEdit("0.1");
        layout->addWidget(dxEdit);

        return layout;
    }

    /**
     * @brief Создает колонку с кнопками управления
     * @return QVBoxLayout* Вертикальный layout с кнопками управления
     */
    QVBoxLayout* createControlColumn()
    {
        QVBoxLayout *layout = new QVBoxLayout();

        QLabel *titleLabel = new QLabel("Управление");
        titleLabel->setAlignment(Qt::AlignCenter);
        titleLabel->setStyleSheet("font-weight: bold; color: #3498db; margin-bottom: 5px;");
        layout->addWidget(titleLabel);

        layout->addStretch();

        calculateButton = new QPushButton("📊 Рассчитать");
        calculateButton->setObjectName("calculateButton");
        calculateButton->setMinimumHeight(45);
        layout->addWidget(calculateButton);

        layout->addSpacing(10);

        clearButton = new QPushButton("🗑️ Очистить");
        clearButton->setObjectName("clearButton");
        clearButton->setMinimumHeight(45);
        layout->addWidget(clearButton);

        layout->addStretch();

        return layout;
    }

    /**
     * @brief Подключает сигналы к слотам
     */
    void connectSignals()
    {
        connect(calculateButton, &QPushButton::clicked, this, &MainWindow::calculateFunction);
        connect(clearButton, &QPushButton::clicked, this, &MainWindow::clearAll);
    }

    /**
     * @brief Вычисляет значения функции для заданного диапазона
     * @param a1 Коэффициент a1 функции
     * @param b1 Коэффициент b1 функции
     * @param a2 Коэффициент a2 функции
     * @param b2 Коэффициент b2 функции
     * @param a3 Коэффициент a3 функции
     * @param b3 Коэффициент b3 функции
     * @param x0 Начальное значение x
     * @param xk Конечное значение x
     * @param dx Шаг изменения x
     * @param xValues Вектор для сохранения значений x
     * @param yValues Вектор для сохранения значений y(x)
     */
    void calculateYFunction(double a1, double b1, double a2, double b2, double a3, double b3,
                          double x0, double xk, double dx,
                          QVector<double> &xValues, QVector<double> &yValues)
    {
        xValues.clear();
        yValues.clear();

        for (double x = x0; x <= xk; x += dx) {
            double y = a1 * qSin(b1 * x) + a2 * qSin(b2 * x) + a3 * qSin(b3 * x);
            xValues.append(x);
            yValues.append(y);
        }
    }

    /**
     * @brief Обновляет таблицу значениями x и y(x)
     * @param xValues Вектор значений x
     * @param yValues Вектор значений y(x)
     */
    void updateTable(const QVector<double> &xValues, const QVector<double> &yValues)
    {
        tableWidget->setRowCount(xValues.size());

        for (int i = 0; i < xValues.size(); ++i) {
            QTableWidgetItem *xItem = new QTableWidgetItem(QString::number(xValues[i], 'f', 4));
            QTableWidgetItem *yItem = new QTableWidgetItem(QString::number(yValues[i], 'f', 4));

            xItem->setTextAlignment(Qt::AlignCenter);
            yItem->setTextAlignment(Qt::AlignCenter);

            tableWidget->setItem(i, 0, xItem);
            tableWidget->setItem(i, 1, yItem);
        }
    }

    /**
     * @brief Обновляет график функции
     * @param xValues Вектор значений x
     * @param yValues Вектор значений y(x)
     */
    void updateChart(const QVector<double> &xValues, const QVector<double> &yValues)
    {
        QLineSeries *series = new QLineSeries();
        series->setColor(QColor("#e74c3c"));
        series->setPen(QPen(QBrush("#e74c3c"), 2));

        for (int i = 0; i < xValues.size(); ++i) {
            series->append(xValues[i], yValues[i]);
        }

        QChart *chart = new QChart();
        chart->setBackgroundBrush(QBrush(QColor("#2c3e50")));
        chart->setTitleBrush(QBrush(QColor("#ecf0f1")));
        chart->legend()->hide();
        chart->addSeries(series);
        chart->setTitle("График функции y(x) = a₁⋅sin(b₁⋅x) + a₂⋅sin(b₂⋅x) + a₃⋅sin(b₃⋅x)");
        chart->setAnimationOptions(QChart::AllAnimations);

        QValueAxis *axisX = new QValueAxis();
        axisX->setTitleText("x");
        axisX->setLabelFormat("%.2f");
        axisX->setTitleBrush(QBrush(QColor("#ecf0f1")));
        axisX->setLabelsColor(QColor("#ecf0f1"));
        axisX->setGridLineColor(QColor("#34495e"));
        chart->addAxis(axisX, Qt::AlignBottom);
        series->attachAxis(axisX);

        QValueAxis *axisY = new QValueAxis();
        axisY->setTitleText("y(x)");
        axisY->setLabelFormat("%.2f");
        axisY->setTitleBrush(QBrush(QColor("#ecf0f1")));
        axisY->setLabelsColor(QColor("#ecf0f1"));
        axisY->setGridLineColor(QColor("#34495e"));
        chart->addAxis(axisY, Qt::AlignLeft);
        series->attachAxis(axisY);

        chartView->setChart(chart);
    }

    /**
     * @brief Показывает диалоговое окно с сообщением об ошибке
     * @param message Текст сообщения об ошибке
     */
    void showError(const QString &message)
    {
        QMessageBox msgBox;
        msgBox.setWindowTitle("Ошибка");
        msgBox.setText(message);
        msgBox.setIcon(QMessageBox::Critical);
        msgBox.setStyleSheet("QMessageBox { background-color: #2c3e50; color: white; }"
                           "QMessageBox QLabel { color: white; }"
                           "QPushButton { background-color: #e74c3c; color: white; border: none; padding: 8px; border-radius: 4px; }");
        msgBox.exec();
    }

    // Элементы UI
    QLineEdit *a1Edit, *b1Edit, *a2Edit, *b2Edit, *a3Edit, *b3Edit; ///< Поля ввода коэффициентов функции
    QLineEdit *x0Edit, *xkEdit, *dxEdit; ///< Поля ввода диапазона и шага
    QPushButton *calculateButton, *clearButton; ///< Кнопки управления
    QTableWidget *tableWidget; ///< Таблица для отображения значений
    QChartView *chartView; ///< Виджет для отображения графика
};

/**
 * @brief Точка входа в приложение
 * @param argc Количество аргументов командной строки
 * @param argv Массив аргументов командной строки
 * @return int Код возврата приложения
 *
 * Создает и запускает главное окно приложения, устанавливает
 * глобальные настройки стиля и шрифтов.
 */
int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    // Установка стиля приложения
    app.setStyle("Fusion");

    // Установка шрифта
    QFont defaultFont("Segoe UI", 10);
    app.setFont(defaultFont);

    MainWindow window;
    window.show();

    return app.exec();
}

#include "main.moc"
