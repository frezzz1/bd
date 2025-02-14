import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTableWidget,
    QTableWidgetItem
)

class LeaveManager(QWidget):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.setWindowTitle("Управление Отпусками")
        self.initUI()
        self.load_leaves()

    def initUI(self):
        layout = QVBoxLayout()

        # Поля ввода для нового отпуска
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("ID Отпуска (для редактирования)")
        layout.addWidget(self.id_input)

        self.employee_id_input = QLineEdit(self)
        self.employee_id_input.setPlaceholderText("ID Сотрудника")
        layout.addWidget(self.employee_id_input)

        self.start_date_input = QLineEdit(self)
        self.start_date_input.setPlaceholderText("Дата начала (YYYY-MM-DD)")
        layout.addWidget(self.start_date_input)

        self.end_date_input = QLineEdit(self)
        self.end_date_input.setPlaceholderText("Дата окончания (YYYY-MM-DD)")
        layout.addWidget(self.end_date_input)

        self.type_input = QLineEdit(self)
        self.type_input.setPlaceholderText("Тип отпуска")
        layout.addWidget(self.type_input)

        # Кнопки для добавления, обновления и удаления отпусков
        self.add_button = QPushButton("Добавить Отпуск", self)
        self.add_button.clicked.connect(self.add_leave)
        layout.addWidget(self.add_button)

        self.update_button = QPushButton("Обновить Отпуск", self)
        self.update_button.clicked.connect(self.update_leave)
        layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Удалить Отпуск", self)
        self.delete_button.clicked.connect(self.delete_leave)
        layout.addWidget(self.delete_button)

        # Таблица для отображения отпусков
        self.leave_table = QTableWidget(self)
        self.leave_table.setColumnCount(5)  # id_leave, id_employee, start_date, end_date, type
        self.leave_table.setHorizontalHeaderLabels(["ID", "ID Сотрудника", "Дата Начала", "Дата Окончания", "Тип"])
        layout.addWidget(self.leave_table)

        # Установка основного макета
        self.setLayout(layout)

    def load_leaves(self):
        # Очистка таблицы перед загрузкой данных
        self.leave_table.setRowCount(0)
        
        try:
            # Получение всех отпусков из базы данных
            self.cursor.execute("SELECT * FROM leave")
            leaves = self.cursor.fetchall()
            
            for row in leaves:
                row_position = self.leave_table.rowCount()
                self.leave_table.insertRow(row_position)
                for column, data in enumerate(row):
                    item = QTableWidgetItem(str(data))
                    self.leave_table.setItem(row_position, column, item)

            QMessageBox.information(self, "Успех", "Данные об отпусках загружены.")
        
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные: {e}")

    def add_leave(self):
        id_text = self.id_input.text()
        employee_id_text = self.employee_id_input.text()
        start_date = self.start_date_input.text()
        end_date = self.end_date_input.text()
        leave_type = self.type_input.text()

        if not id_text or not employee_id_text or not start_date or not end_date or not leave_type:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            leave_id = int(id_text)  # Преобразуем ID отпуска в целое число
            employee_id = int(employee_id_text)  # Преобразуем ID сотрудника в целое число

            # Добавление нового отпуска в базу данных
            query = """
                INSERT INTO leave (id_leave, id_employee, start_date, end_date, type) VALUES (%s, %s, %s, %s, %s)
            """
            values = (leave_id, employee_id, start_date, end_date, leave_type)

            self.cursor.execute(query, values)
            # Сохранение изменений
            self.cursor.connection.commit()
            QMessageBox.information(self, "Успех", "Отпуск добавлен успешно!")
            self.load_leaves()  # Обновление списка отпусков

            # Очистка полей ввода
            self.id_input.clear()
            self.employee_id_input.clear()
            self.start_date_input.clear()
            self.end_date_input.clear()
            self.type_input.clear()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить отпуск: {e}")

    def update_leave(self):
        selected_row = self.leave_table.currentRow()
    
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите отпуск для обновления.")
            return
    
        old_leave_id_text = str(self.leave_table.item(selected_row, 0).text())
    
        new_leave_id_text = self.id_input.text()
        employee_id_text = self.employee_id_input.text()
        start_date = self.start_date_input.text()
        end_date = self.end_date_input.text()
        leave_type = self.type_input.text()

        if not new_leave_id_text or not employee_id_text or not start_date or not end_date or not leave_type:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            old_leave_id = int(old_leave_id_text)  # Старый ID отпуска для обновления
            new_leave_id = int(new_leave_id_text)  # Новый ID отпуска

            # Обновление отпуска в базе данных
            query = """
                UPDATE leave SET id_leave=%s, id_employee=%s, start_date=%s, end_date=%s, type=%s WHERE id_leave=%s
            """
            values = (new_leave_id, int(employee_id_text), start_date, end_date, leave_type, old_leave_id)

            # Выполнение запроса на обновление
            self.cursor.execute(query, values)
        
            # Сохранение изменений
            self.cursor.connection.commit()
            QMessageBox.information(self, "Успех", "Отпуск обновлен успешно!")
            self.load_leaves()  # Обновление списка отпусков

            # Очистка полей ввода
            self.id_input.clear()
            self.employee_id_input.clear()
            self.start_date_input.clear()
            self.end_date_input.clear()
            self.type_input.clear()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось обновить отпуск: {e}")

    def delete_leave(self):
        selected_row = self.leave_table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста выберите отпуск для удаления.")
            return
    
        leave_id = int(self.leave_table.item(selected_row, 0).text())

        try:
            # Удаление отпуска из базы данных
            query = """
                DELETE FROM leave WHERE id_leave=%s
            """
        
            self.cursor.execute(query, (leave_id,))
        
             # Сохранение изменений
            self.cursor.connection.commit() 
         
            QMessageBox.information(self, "Успех", "Отпуск удален успешно!")
            self.load_leaves()  # Обновление списка отпусков

        except Exception as e:
             QMessageBox.warning(self, "Ошибка", f"Не удалось удалить отпуск: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LeaveManager(None)  # Передайте курсор позже в основном приложении
    window.show()
    sys.exit(app.exec_())
