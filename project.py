import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTableWidget,
    QTableWidgetItem, QApplication
)

class ProjectManager(QWidget):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.setWindowTitle("Управление Проектами")
        self.initUI()
        self.load_projects()

    def initUI(self):
        layout = QVBoxLayout()

        # Поля ввода для нового проекта
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("ID Проекта (для редактирования)")
        layout.addWidget(self.id_input)

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Название проекта")
        layout.addWidget(self.title_input)

        self.start_date_input = QLineEdit(self)
        self.start_date_input.setPlaceholderText("Дата начала (YYYY-MM-DD)")
        layout.addWidget(self.start_date_input)

        self.end_date_input = QLineEdit(self)
        self.end_date_input.setPlaceholderText("Дата окончания (YYYY-MM-DD)")
        layout.addWidget(self.end_date_input)

        self.status_input = QLineEdit(self)
        self.status_input.setPlaceholderText("Статус проекта")
        layout.addWidget(self.status_input)

        # Кнопки для добавления, обновления и удаления проектов
        self.add_button = QPushButton("Добавить Проект", self)
        self.add_button.clicked.connect(self.add_project)
        layout.addWidget(self.add_button)

        self.update_button = QPushButton("Обновить Проект", self)
        self.update_button.clicked.connect(self.update_project)
        layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Удалить Проект", self)
        self.delete_button.clicked.connect(self.delete_project)
        layout.addWidget(self.delete_button)

        # Таблица для отображения проектов
        self.project_table = QTableWidget(self)
        self.project_table.setColumnCount(5)  # id_project, title, start_date, end_date, status
        self.project_table.setHorizontalHeaderLabels(["ID", "Название", "Дата начала", "Дата окончания", "Статус"])
        layout.addWidget(self.project_table)

        # Установка основного макета
        self.setLayout(layout)

    def load_projects(self):
        # Очистка таблицы перед загрузкой данных
        self.project_table.setRowCount(0)
        
        try:
            # Получение всех проектов из базы данных
            self.cursor.execute("SELECT * FROM project")
            projects = self.cursor.fetchall()
            
            for row in projects:
                row_position = self.project_table.rowCount()
                self.project_table.insertRow(row_position)
                for column, data in enumerate(row):
                    item = QTableWidgetItem(str(data))
                    self.project_table.setItem(row_position, column, item)

            QMessageBox.information(self, "Успех", "Данные о проектах загружены.")
        
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные: {e}")

    def add_project(self):
        id_text = self.id_input.text()
        title = self.title_input.text()
        start_date = self.start_date_input.text()
        end_date = self.end_date_input.text()
        status = self.status_input.text()

        if not id_text or not title or not start_date or not end_date or not status:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            project_id = int(id_text)  # Преобразуем ID проекта в целое число

            # Добавление нового проекта в базу данных
            query = """
                INSERT INTO project (id_project, title, start_date, end_date, status) VALUES (%s, %s, %s, %s, %s)
            """
            values = (project_id, title, start_date, end_date, status)

            self.cursor.execute(query, values)
            # Сохранение изменений
            self.cursor.connection.commit()
            QMessageBox.information(self, "Успех", "Проект добавлен успешно!")
            self.load_projects()  # Обновление списка проектов

            # Очистка полей ввода
            self.id_input.clear()
            self.title_input.clear()
            self.start_date_input.clear()
            self.end_date_input.clear()
            self.status_input.clear()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить проект: {e}")

    def update_project(self):
        selected_row = self.project_table.currentRow()
        
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите проект для обновления.")
            return
        
        old_project_id_text = str(self.project_table.item(selected_row, 0).text())
        
        new_project_id_text = self.id_input.text()
        
        title = self.title_input.text()
        start_date = self.start_date_input.text()
        end_date = self.end_date_input.text()
        status = self.status_input.text()

        if not new_project_id_text or not title or not start_date or not end_date or not status:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            old_project_id = int(old_project_id_text)  # Старый ID проекта для обновления
            new_project_id = int(new_project_id_text)  # Новый ID проекта

            # Обновление проекта в базе данных
            query = """
                UPDATE project SET id_project=%s, title=%s, start_date=%s, end_date=%s, status=%s WHERE id_project=%s
            """
            values = (new_project_id, title, start_date, end_date, status, old_project_id)

            # Выполнение запроса на обновление
            self.cursor.execute(query, values)
            
            # Сохранение изменений
            self.cursor.connection.commit()
            QMessageBox.information(self, "Успех", "Проект обновлен успешно!")
            self.load_projects()  # Обновление списка проектов

            # Очистка полей ввода
            self.id_input.clear()
            self.title_input.clear()
            self.start_date_input.clear()
            self.end_date_input.clear()
            self.status_input.clear()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось обновить проект: {e}")

    def delete_project(self):
        selected_row = self.project_table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите проект для удаления.")
            return
        
        project_id = int(self.project_table.item(selected_row, 0).text())

        try:
            # Удаление проекта из базы данных
            query = """
                DELETE FROM project WHERE id_project=%s
            """
            
            self.cursor.execute(query, (project_id,))
            
            # Сохранение изменений
            self.cursor.connection.commit()
            
            QMessageBox.information(self, "Успех", "Проект удален успешно!")
            self.load_projects()  # Обновление списка проектов

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить проект: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProjectManager(None)  # Передайте курсор позже в основном приложении
    window.show()
    sys.exit(app.exec_())
