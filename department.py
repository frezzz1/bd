import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTableWidget,
    QTableWidgetItem
)

class DepartmentManager(QWidget):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.setWindowTitle("Управление Отделами")
        self.initUI()
        self.load_departments()

    def initUI(self):
        layout = QVBoxLayout()

        # Поля ввода для нового отдела
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("ID Отдела (для редактирования)")
        layout.addWidget(self.id_input)

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Название отдела")
        layout.addWidget(self.title_input)

        self.director_input = QLineEdit(self)
        self.director_input.setPlaceholderText("ID Директора")
        layout.addWidget(self.director_input)

        self.location_input = QLineEdit(self)
        self.location_input.setPlaceholderText("Местоположение")
        layout.addWidget(self.location_input)

        # Кнопки для добавления, обновления и удаления отделов
        self.add_button = QPushButton("Добавить Отдел", self)
        self.add_button.clicked.connect(self.add_department)
        layout.addWidget(self.add_button)

        self.update_button = QPushButton("Обновить Отдел", self)
        self.update_button.clicked.connect(self.update_department)
        layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Удалить Отдел", self)
        self.delete_button.clicked.connect(self.delete_department)
        layout.addWidget(self.delete_button)

        # Таблица для отображения отделов
        self.department_table = QTableWidget(self)
        self.department_table.setColumnCount(4)  # id_department, title, id_director, location
        self.department_table.setHorizontalHeaderLabels(["ID", "Название", "ID Директора", "Местоположение"])
        layout.addWidget(self.department_table)

        # Установка основного макета
        self.setLayout(layout)

    def load_departments(self):
        # Очистка таблицы перед загрузкой данных
        self.department_table.setRowCount(0)
        
        try:
            # Получение всех отделов из базы данных
            self.cursor.execute("SELECT * FROM department")
            departments = self.cursor.fetchall()
            
            for row in departments:
                row_position = self.department_table.rowCount()
                self.department_table.insertRow(row_position)
                for column, data in enumerate(row):
                    item = QTableWidgetItem(str(data))
                    self.department_table.setItem(row_position, column, item)

            QMessageBox.information(self, "Успех", "Данные об отделах загружены.")
        
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные: {e}")

    def add_department(self):
        id_text = self.id_input.text()
        title = self.title_input.text()
        director_id_text = self.director_input.text()
        location = self.location_input.text()

        if not id_text or not title or not director_id_text or not location:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            department_id = int(id_text)  # Преобразуем ID отдела в целое число
            director_id = int(director_id_text)  # Преобразуем ID директора в целое число

            # Добавление нового отдела в базу данных
            query = """
                INSERT INTO department (id_department, title, id_director, location) VALUES (%s, %s, %s, %s)
            """
            values = (department_id, title, director_id, location)

            self.cursor.execute(query, values)
            # Сохранение изменений
            self.cursor.connection.commit()
            QMessageBox.information(self, "Успех", "Отдел добавлен успешно!")
            self.load_departments()  # Обновление списка отделов

            # Очистка полей ввода
            self.id_input.clear()
            self.title_input.clear()
            self.director_input.clear()
            self.location_input.clear()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить отдел: {e}")

    def update_department(self):
        selected_row = self.department_table.currentRow()
        
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите отдел для обновления.")
            return
        
        old_department_id_text = str(self.department_table.item(selected_row, 0).text())
        
        new_department_id_text = self.id_input.text()
        
        title = self.title_input.text()
        director_id_text = self.director_input.text()
        location = self.location_input.text()

        if not new_department_id_text or not title or not director_id_text or not location:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            old_department_id = int(old_department_id_text)  # Старый ID отдела для обновления
            new_department_id = int(new_department_id_text)  # Новый ID отдела

            # Обновление отдела в базе данных
            query = """
                UPDATE department SET id_department=%s, title=%s, id_director=%s, location=%s WHERE id_department=%s
            """
            values = (new_department_id, title, int(director_id_text), location, old_department_id)

            # Выполнение запроса на обновление
            self.cursor.execute(query, values)
            
            # Сохранение изменений
            self.cursor.connection.commit()
            QMessageBox.information(self, "Успех", "Отдел обновлен успешно!")
            self.load_departments()  # Обновление списка отделов

            # Очистка полей ввода
            self.id_input.clear()
            self.title_input.clear()
            self.director_input.clear()
            self.location_input.clear()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось обновить отдел: {e}")

    def delete_department(self):
        selected_row = self.department_table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите отдел для удаления.")
            return
        
        department_id = int(self.department_table.item(selected_row, 0).text())

        try:
            # Удаление отдела из базы данных
            query = """
                DELETE FROM department WHERE id_department=%s
            """
            
            self.cursor.execute(query, (department_id,))
            
            # Сохранение изменений
            self.cursor.connection.commit()
            
            QMessageBox.information(self, "Успех", "Отдел удален успешно!")
            self.load_departments()  # Обновление списка отделов

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить отдел: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DepartmentManager(None)  # Передайте курсор позже в основном приложении
    window.show()
    sys.exit(app.exec_())
