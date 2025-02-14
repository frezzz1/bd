import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QMessageBox, QTableWidget,
    QTableWidgetItem, QApplication
)

class TrainingManager(QWidget):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.setWindowTitle("Управление Обучением")
        self.initUI()
        self.load_trainings()

    def initUI(self):
        layout = QVBoxLayout()

        # Поля ввода для новой тренировки
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("ID Тренировки (для редактирования)")
        layout.addWidget(self.id_input)

        self.employee_id_input = QLineEdit(self)
        self.employee_id_input.setPlaceholderText("ID Сотрудника")
        layout.addWidget(self.employee_id_input)

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Название тренировки")
        layout.addWidget(self.title_input)

        self.start_date_input = QLineEdit(self)
        self.start_date_input.setPlaceholderText("Дата начала (YYYY-MM-DD)")
        layout.addWidget(self.start_date_input)

        self.end_date_input = QLineEdit(self)
        self.end_date_input.setPlaceholderText("Дата окончания (YYYY-MM-DD)")
        layout.addWidget(self.end_date_input)

        self.result_input = QLineEdit(self)
        self.result_input.setPlaceholderText("Результат тренировки")
        layout.addWidget(self.result_input)

        # Кнопки для добавления, обновления и удаления тренировок
        self.add_button = QPushButton("Добавить Тренировку", self)
        self.add_button.clicked.connect(self.add_training)
        layout.addWidget(self.add_button)

        self.update_button = QPushButton("Обновить Тренировку", self)
        self.update_button.clicked.connect(self.update_training)
        layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Удалить Тренировку", self)
        self.delete_button.clicked.connect(self.delete_training)
        layout.addWidget(self.delete_button)

        # Таблица для отображения тренировок
        self.training_table = QTableWidget(self)
        self.training_table.setColumnCount(6)  # id_training, id_employee, title, start_date, end_date, result
        self.training_table.setHorizontalHeaderLabels(["ID", "ID Сотрудника", "Название", "Дата начала", "Дата окончания", "Результат"])
        layout.addWidget(self.training_table)

        # Установка основного макета
        self.setLayout(layout)

    def load_trainings(self):
        # Очистка таблицы перед загрузкой данных
        self.training_table.setRowCount(0)
        
        try:
            # Получение всех тренировок из базы данных
            self.cursor.execute("SELECT * FROM training")
            trainings = self.cursor.fetchall()
            
            for row in trainings:
                row_position = self.training_table.rowCount()
                self.training_table.insertRow(row_position)
                for column, data in enumerate(row):
                    item = QTableWidgetItem(str(data))
                    self.training_table.setItem(row_position, column, item)

            QMessageBox.information(self, "Успех", "Данные о тренировках загружены.")
        
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные: {e}")

    def add_training(self):
        id_text = self.id_input.text()
        employee_id_text = self.employee_id_input.text()
        title = self.title_input.text()
        start_date = self.start_date_input.text()
        end_date = self.end_date_input.text()
        result = self.result_input.text()

        if not id_text or not employee_id_text or not title or not start_date or not end_date or not result:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            training_id = int(id_text)  # Преобразуем ID тренировки в целое число
            employee_id = int(employee_id_text)  # Преобразуем ID сотрудника в целое число

            # Добавление новой тренировки в базу данных
            query = """
                INSERT INTO training (id_training, id_employee, title, start_date, end_date, result) VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (training_id, employee_id, title, start_date, end_date, result)

            self.cursor.execute(query, values)
            # Сохранение изменений
            self.cursor.connection.commit()
            QMessageBox.information(self, "Успех", "Тренировка добавлена успешно!")
            self.load_trainings()  # Обновление списка тренировок

            # Очистка полей ввода
            self.id_input.clear()
            self.employee_id_input.clear()
            self.title_input.clear()
            self.start_date_input.clear()
            self.end_date_input.clear()
            self.result_input.clear()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить тренировку: {e}")

    def update_training(self):
        selected_row = self.training_table.currentRow()
        
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите тренировку для обновления.")
            return
        
        old_training_id_text = str(self.training_table.item(selected_row, 0).text())
        
        new_training_id_text = self.id_input.text()
        
        employee_id_text = self.employee_id_input.text()
        title = self.title_input.text()
        start_date = self.start_date_input.text()
        end_date = self.end_date_input.text()
        result = self.result_input.text()

        if not new_training_id_text or not employee_id_text or not title or not start_date or not end_date or not result:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            old_training_id = int(old_training_id_text)  # Старый ID тренировки для обновления
            new_training_id = int(new_training_id_text)  # Новый ID тренировки

            # Обновление тренировки в базе данных
            query = """
                UPDATE training SET id_training=%s, id_employee=%s, title=%s, start_date=%s, end_date=%s, result=%s WHERE id_training=%s
            """
            values = (new_training_id, int(employee_id_text), title, start_date, end_date, result, old_training_id)

            # Выполнение запроса на обновление
            self.cursor.execute(query, values)
            
            # Сохранение изменений
            self.cursor.connection.commit()
            QMessageBox.information(self, "Успех", "Тренировка обновлена успешно!")
            self.load_trainings()  # Обновление списка тренировок

            # Очистка полей ввода
            self.id_input.clear()
            self.employee_id_input.clear()
            self.title_input.clear()
            self.start_date_input.clear()
            self.end_date_input.clear()
            self.result_input.clear()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось обновить тренировку: {e}")

    def delete_training(self):
        selected_row = self.training_table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите тренировку для удаления.")
            return
        
        training_id = int(self.training_table.item(selected_row, 0).text())

        try:
            # Удаление тренировки из базы данных
            query = """
                DELETE FROM training WHERE id_training=%s
            """
            
            self.cursor.execute(query, (training_id,))
            
            # Сохранение изменений
            self.cursor.connection.commit()
            
            QMessageBox.information(self, "Успех", "Тренировка удалена успешно!")
            self.load_trainings()  # Обновление списка тренировок

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить тренировку: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainingManager(None)  # Передайте курсор позже в основном приложении
    window.show()
    sys.exit(app.exec_())
