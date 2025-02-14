import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QMessageBox, QTableWidget,
    QTableWidgetItem, QApplication
)

class ProjectParticipationManager(QWidget):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.setWindowTitle("Управление Участием в Проектах")
        self.initUI()
        self.load_participations()

    def initUI(self):
        layout = QVBoxLayout()

        # Поля ввода для нового участия
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("ID Участия (для редактирования)")
        layout.addWidget(self.id_input)

        self.employee_id_input = QLineEdit(self)
        self.employee_id_input.setPlaceholderText("ID Сотрудника")
        layout.addWidget(self.employee_id_input)

        self.project_id_input = QLineEdit(self)
        self.project_id_input.setPlaceholderText("ID Проекта")
        layout.addWidget(self.project_id_input)

        self.role_input = QLineEdit(self)
        self.role_input.setPlaceholderText("Роль в проекте")
        layout.addWidget(self.role_input)

        # Кнопки для добавления, обновления и удаления участия
        self.add_button = QPushButton("Добавить Участие", self)
        self.add_button.clicked.connect(self.add_participation)
        layout.addWidget(self.add_button)

        self.update_button = QPushButton("Обновить Участие", self)
        self.update_button.clicked.connect(self.update_participation)
        layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Удалить Участие", self)
        self.delete_button.clicked.connect(self.delete_participation)
        layout.addWidget(self.delete_button)

        # Таблица для отображения участия
        self.participation_table = QTableWidget(self)
        self.participation_table.setColumnCount(4)  # id_participation, id_employee, id_project, role
        self.participation_table.setHorizontalHeaderLabels(["ID", "ID Сотрудника", "ID Проекта", "Роль"])
        layout.addWidget(self.participation_table)

        # Установка основного макета
        self.setLayout(layout)

    def load_participations(self):
        # Очистка таблицы перед загрузкой данных
        self.participation_table.setRowCount(0)
        
        try:
            # Получение всех записей об участии из базы данных
            self.cursor.execute("SELECT * FROM project_participation")
            participations = self.cursor.fetchall()
            
            for row in participations:
                row_position = self.participation_table.rowCount()
                self.participation_table.insertRow(row_position)
                for column, data in enumerate(row):
                    item = QTableWidgetItem(str(data))
                    self.participation_table.setItem(row_position, column, item)

            QMessageBox.information(self, "Успех", "Данные об участии загружены.")
        
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные: {e}")

    def add_participation(self):
        id_text = self.id_input.text()
        employee_id_text = self.employee_id_input.text()
        project_id_text = self.project_id_input.text()
        role = self.role_input.text()

        if not id_text or not employee_id_text or not project_id_text or not role:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            participation_id = int(id_text)  # Преобразуем ID участия в целое число
            employee_id = int(employee_id_text)  # Преобразуем ID сотрудника в целое число
            project_id = int(project_id_text)  # Преобразуем ID проекта в целое число

            # Добавление нового участия в базу данных
            query = """
                INSERT INTO project_participation (id_participation, id_employee, id_project, role) VALUES (%s, %s, %s, %s)
            """
            values = (participation_id, employee_id, project_id, role)

            self.cursor.execute(query, values)
            # Сохранение изменений
            self.cursor.connection.commit()
            QMessageBox.information(self, "Успех", "Участие добавлено успешно!")
            self.load_participations()  # Обновление списка участия

            # Очистка полей ввода
            self.id_input.clear()
            self.employee_id_input.clear()
            self.project_id_input.clear()
            self.role_input.clear()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить участие: {e}")

    def update_participation(self):
        selected_row = self.participation_table.currentRow()
        
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите участие для обновления.")
            return
        
        old_participation_id_text = str(self.participation_table.item(selected_row, 0).text())
        
        new_participation_id_text = self.id_input.text()
        
        employee_id_text = self.employee_id_input.text()
        project_id_text = self.project_id_input.text()
        role = self.role_input.text()

        if not new_participation_id_text or not employee_id_text or not project_id_text or not role:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            old_participation_id = int(old_participation_id_text)  # Старый ID участия для обновления
            new_participation_id = int(new_participation_id_text)  # Новый ID участия

            # Обновление участия в базе данных
            query = """
                UPDATE project_participation SET id_participation=%s, id_employee=%s, id_project=%s, role=%s WHERE id_participation=%s
            """
            values = (new_participation_id, int(employee_id_text), int(project_id_text), role, old_participation_id)

            # Выполнение запроса на обновление
            self.cursor.execute(query, values)
            
            # Сохранение изменений
            self.cursor.connection.commit()
            QMessageBox.information(self, "Успех", "Участие обновлено успешно!")
            self.load_participations()  # Обновление списка участия

            # Очистка полей ввода
            self.id_input.clear()
            self.employee_id_input.clear()
            self.project_id_input.clear()
            self.role_input.clear()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось обновить участие: {e}")

    def delete_participation(self):
        selected_row = self.participation_table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите участие для удаления.")
            return
        
        participation_id = int(self.participation_table.item(selected_row, 0).text())

        try:
            # Удаление участия из базы данных
            query = """
                DELETE FROM project_participation WHERE id_participation=%s
            """
            
            self.cursor.execute(query, (participation_id,))
            
            # Сохранение изменений
            self.cursor.connection.commit()
            
            QMessageBox.information(self, "Успех", "Участие удалено успешно!")
            self.load_participations()  # Обновление списка участия

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить участие: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProjectParticipationManager(None)  # Передайте курсор позже в основном приложении
    window.show()
    sys.exit(app.exec_())
