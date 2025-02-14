import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTableWidget,
    QTableWidgetItem
)

class PositionManager(QWidget):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.setWindowTitle("Управление Должностями")
        self.initUI()
        self.load_positions()

    def initUI(self):
        layout = QVBoxLayout()

        # Поля ввода для новой должности
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("ID Должности (для добавления)")
        layout.addWidget(self.id_input)

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Название должности")
        layout.addWidget(self.title_input)

        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Описание должности")
        layout.addWidget(self.description_input)

        # Кнопки для добавления, обновления и удаления должностей
        self.add_button = QPushButton("Добавить Должность", self)
        self.add_button.clicked.connect(self.add_position)
        layout.addWidget(self.add_button)

        self.update_button = QPushButton("Обновить Должность", self)
        self.update_button.clicked.connect(self.update_position)
        layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Удалить Должность", self)
        self.delete_button.clicked.connect(self.delete_position)
        layout.addWidget(self.delete_button)

        # Таблица для отображения должностей
        self.position_table = QTableWidget(self)
        self.position_table.setColumnCount(3)  # id_position, title, description
        self.position_table.setHorizontalHeaderLabels(["ID", "Название", "Описание"])
        layout.addWidget(self.position_table)

        # Установка основного макета
        self.setLayout(layout)

    def load_positions(self):
        # Очистка таблицы перед загрузкой данных
        self.position_table.setRowCount(0)
        
        try:
            # Получение всех должностей из базы данных
            self.cursor.execute("SELECT * FROM position")
            positions = self.cursor.fetchall()
            
            for row in positions:
                row_position = self.position_table.rowCount()
                self.position_table.insertRow(row_position)
                for column, data in enumerate(row):
                    item = QTableWidgetItem(str(data))
                    self.position_table.setItem(row_position, column, item)

            QMessageBox.information(self, "Успех", "Данные о должностях загружены.")
        
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные: {e}")

    def add_position(self):
        id_text = self.id_input.text()
        title = self.title_input.text()
        description = self.description_input.text()

        if not id_text or not title or not description:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            position_id = int(id_text)  # Преобразуем ID должности в целое число

            # Добавление новой должности в базу данных
            query = """
                INSERT INTO position (id_position, title, description) VALUES (%s, %s, %s)
            """
            values = (position_id, title, description)

            self.cursor.execute(query, values)
            # Сохранение изменений
            self.cursor.connection.commit()
            QMessageBox.information(self, "Успех", "Должность добавлена успешно!")
            self.load_positions()  # Обновление списка должностей

            # Очистка полей ввода
            self.id_input.clear()
            self.title_input.clear()
            self.description_input.clear()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить должность: {e}")

    def update_position(self):
        selected_row = self.position_table.currentRow()
        
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите должность для обновления.")
            return
        
        old_position_id_text = str(self.position_table.item(selected_row, 0).text())
        
        new_position_id_text = self.id_input.text()
        
        title = self.title_input.text()
        description = self.description_input.text()

        if not new_position_id_text or not title or not description:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            old_position_id = int(old_position_id_text)  # Старый ID должности для обновления
            new_position_id = int(new_position_id_text)  # Новый ID должности

            # Обновление должности в базе данных
            query = """
                UPDATE position SET id_position=%s, title=%s, description=%s WHERE id_position=%s
            """
            values = (new_position_id, title, description, old_position_id)

            # Выполнение запроса на обновление
            self.cursor.execute(query, values)
            
            # Сохранение изменений
            self.cursor.connection.commit()
            QMessageBox.information(self, "Успех", "Должность обновлена успешно!")
            self.load_positions()  # Обновление списка должностей

            # Очистка полей ввода
            self.id_input.clear()
            self.title_input.clear()
            self.description_input.clear()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось обновить должность: {e}")

    def delete_position(self):
        selected_row = self.position_table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста выберите должность для удаления.")
            return
        
        position_id = int(self.position_table.item(selected_row, 0).text())

        try:
            # Удаление должности из базы данных
            query = """
                DELETE FROM position WHERE id_position=%s
            """
            
            self.cursor.execute(query, (position_id,))
            
            # Сохранение изменений
            self.cursor.connection.commit()
            
            QMessageBox.information(self, "Успех", "Должность удалена успешно!")
            self.load_positions()  # Обновление списка должностей

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить должность: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PositionManager(None)  # Передайте курсор позже в основном приложении
    window.show()
    sys.exit(app.exec_())
