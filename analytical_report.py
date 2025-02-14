import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QMessageBox,
    QTableWidget, QTableWidgetItem, QLabel
)

class AnalyticalReportManager(QWidget):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.setWindowTitle("Аналитические Отчеты")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Кнопка для отчета по зарплатам сотрудников
        self.salary_report_button = QPushButton("Отчет по Зарплатам", self)
        self.salary_report_button.clicked.connect(self.generate_salary_report)
        layout.addWidget(self.salary_report_button)

        # Кнопка для отчета по участию в проектах
        self.participation_report_button = QPushButton("Отчет по Участию в Проектах", self)
        self.participation_report_button.clicked.connect(self.generate_participation_report)
        layout.addWidget(self.participation_report_button)

        # Таблица для отображения результатов отчетов
        self.report_table = QTableWidget(self)
        layout.addWidget(self.report_table)

        # Установка основного макета
        self.setLayout(layout)

    def generate_salary_report(self):
        try:
            # Запрос для получения средней, минимальной и максимальной зарплаты по отделам
            query = """
                SELECT d.title AS department_title,
                       AVG(e.salary) AS average_salary,
                       MIN(e.salary) AS min_salary,
                       MAX(e.salary) AS max_salary
                FROM employee e
                JOIN department d ON e.id_department = d.id_department
                GROUP BY d.title;
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            # Обновление таблицы с результатами
            self.report_table.setRowCount(0)
            self.report_table.setColumnCount(4)
            self.report_table.setHorizontalHeaderLabels(["Отдел", "Средняя Зарплата", "Минимальная Зарплата", "Максимальная Зарплата"])

            for row in results:
                row_position = self.report_table.rowCount()
                self.report_table.insertRow(row_position)
                for column, data in enumerate(row):
                    item = QTableWidgetItem(str(data))
                    self.report_table.setItem(row_position, column, item)

            QMessageBox.information(self, "Успех", "Отчет по зарплатам сгенерирован.")

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сгенерировать отчет: {e}")

    def generate_participation_report(self):
        try:
            # Запрос для получения количества проектов, в которых участвовал каждый сотрудник
            query = """
                SELECT e.surname || ' ' || e.name AS employee_name,
                       COUNT(pp.id_project) AS project_count
                FROM employee e
                LEFT JOIN project_participation pp ON e.id_employee = pp.id_employee
                GROUP BY e.id_employee;
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            # Обновление таблицы с результатами
            self.report_table.setRowCount(0)
            self.report_table.setColumnCount(2)
            self.report_table.setHorizontalHeaderLabels(["Сотрудник", "Количество Проектов"])

            for row in results:
                row_position = self.report_table.rowCount()
                self.report_table.insertRow(row_position)
                for column, data in enumerate(row):
                    item = QTableWidgetItem(str(data))
                    self.report_table.setItem(row_position, column, item)

            QMessageBox.information(self, "Успех", "Отчет по участию в проектах сгенерирован.")

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сгенерировать отчет: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnalyticalReportManager(None)  # Передайте курсор позже в основном приложении
    window.show()
    sys.exit(app.exec_())
