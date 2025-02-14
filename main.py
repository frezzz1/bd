import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon

# Импортируем модули для каждой вкладки
from department import DepartmentManager
from position import PositionManager
from employee import EmployeeManager
from project import ProjectManager
from training import TrainingManager
from project_participation import ProjectParticipationManager
from leave import LeaveManager
from analytical_report import AnalyticalReportManager

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление Персоналом")
        self.setGeometry(100, 100, 800, 600)

        # Подключение к базе данных
        self.connect_to_database()

        # Создание виджета вкладок
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Добавление вкладок
        self.add_tabs()
        
        # Применение стилей
        self.apply_styles()

    def connect_to_database(self):
        try:
            # Параметры подключения (можно вынести в отдельный файл конфигурации)
            self.connection = psycopg2.connect(
                host="localhost",
                user="postgres",
                password="1234",
                database="employee_db"
            )
            print("Подключение к базе данных успешно установлено.")
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")

    def add_tabs(self):
        # Создаем экземпляры всех менеджеров и добавляем их как вкладки с иконками
        self.tabs.addTab(DepartmentManager(self.cursor), QIcon('icons/department.png'), "Отделы")
        self.tabs.addTab(PositionManager(self.cursor), QIcon('icons/position.png'), "Должности")
        self.tabs.addTab(EmployeeManager(self.cursor), QIcon('icons/employee.png'), "Сотрудники")
        self.tabs.addTab(ProjectManager(self.cursor), QIcon('icons/project.png'), "Проекты")
        self.tabs.addTab(TrainingManager(self.cursor), QIcon('icons/training.png'), "Обучение")
        self.tabs.addTab(ProjectParticipationManager(self.cursor), QIcon('icons/participation.png'), "Участие в Проектах")
        self.tabs.addTab(LeaveManager(self.cursor), QIcon('icons/leave.png'), "Отпуска")
        self.tabs.addTab(AnalyticalReportManager(self.cursor), QIcon('icons/report.png'), "Аналитические Отчеты")

    def apply_styles(self):
        """Применение стилей к приложению"""
        
        style = """
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
            }
            QTabBar::tab {
                background: #e0e0e0;
                padding: 10px;
                margin: 0px;
                border: 1px solid #ccc;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                border-bottom: 1px solid white; /* Скрываем нижнюю границу */
            }
            QPushButton {
                background-color: #4CAF50; /* Зеленый цвет */
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Темно-зеленый цвет при наведении */
            }
            QLabel {
                font-size: 14px;
            }
        """
        
        self.setStyleSheet(style)

    def closeEvent(self, event):
        # Закрытие соединения при закрытии приложения
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'connection'):
            self.connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
