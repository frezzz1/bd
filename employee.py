import sys
import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTableWidget,
    QTableWidgetItem, QFileDialog, QApplication,
    QHBoxLayout, QComboBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class EmployeeManager(QWidget):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.setWindowTitle("Управление Сотрудниками")
        self.initUI()
        self.load_employees()

    def initUI(self):
        layout = QVBoxLayout()

        # Поля ввода для нового сотрудника
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("ID Сотрудника (для редактирования)")
        layout.addWidget(self.id_input)

        self.surname_input = QLineEdit(self)
        self.surname_input.setPlaceholderText("Фамилия")
        layout.addWidget(self.surname_input)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Имя")
        layout.addWidget(self.name_input)

        self.birthday_input = QLineEdit(self)
        self.birthday_input.setPlaceholderText("Дата рождения (YYYY-MM-DD)")
        layout.addWidget(self.birthday_input)

        self.date_of_employment_input = QLineEdit(self)
        self.date_of_employment_input.setPlaceholderText("Дата приема на работу (YYYY-MM-DD)")
        layout.addWidget(self.date_of_employment_input)

        self.salary_input = QLineEdit(self)
        self.salary_input.setPlaceholderText("Зарплата")
        layout.addWidget(self.salary_input)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Телефон")
        layout.addWidget(self.phone_input)

        self.id_department_input = QLineEdit(self)
        self.id_department_input.setPlaceholderText("ID Отдела")
        layout.addWidget(self.id_department_input)

        self.id_position_input = QLineEdit(self)
        self.id_position_input.setPlaceholderText("ID Должности")
        layout.addWidget(self.id_position_input)

        # Кнопки для добавления, обновления и удаления сотрудников
        button_layout = QHBoxLayout()
    
        self.add_button = QPushButton("Добавить Сотрудника", self)
        self.add_button.clicked.connect(self.add_employee)
        button_layout.addWidget(self.add_button)

        self.update_button = QPushButton("Обновить Сотрудника", self)
        self.update_button.clicked.connect(self.update_employee)
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Удалить Сотрудника", self)
        self.delete_button.clicked.connect(self.delete_employee)
        button_layout.addWidget(self.delete_button)

         # Кнопка для загрузки фотографии
         # Добавление кнопки загрузки фото
     
        self.upload_photo_button = QPushButton("Загрузить Фото", self)
        self.upload_photo_button.clicked.connect(self.upload_photo)
        button_layout.addWidget(self.upload_photo_button)
        self.delete_photo_button = QPushButton("Удалить Фото", self)
        self.delete_photo_button.clicked.connect(self.delete_photo)
        button_layout.addWidget(self.delete_photo_button)


        layout.addLayout(button_layout)

         # Поля для поиска и фильтрации
        search_layout = QHBoxLayout()
    
         # Поле для поиска
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Поиск по ФИО...")
    
        search_button = QPushButton("Поиск", self)
        search_button.clicked.connect(self.search_employee)

        search_layout.addWidget(search_button)  # Добавляем кнопку поиска
        search_layout.addWidget(self.search_input)  # Добавляем поле поиска

         # Выпадающий список для сортировки
         # Добавление выпадающего списка для выбора поля сортировки
     
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Сортировать по", "Фамилия", "Имя", "Зарплата"])
     
        sort_button = QPushButton("Сортировать", self)
        sort_button.clicked.connect(self.sort_employees)

        search_layout.addWidget(sort_button)  # Добавляем кнопку сортировки после выпадающего списка
        search_layout.addWidget(self.sort_combo)  # Добавляем выпадающий список

        layout.addLayout(search_layout)  # Добавляем поиск и сортировку в основной макет

         # Таблица для отображения сотрудников
        self.employee_table = QTableWidget(self)
     
         # Установка заголовков столбцов
         # id_employee, surname, name, birthday, date_of_employment, salary, email, phone, photo
     
         # Установка заголовков столбцов
        self.employee_table.setColumnCount(11)  
        self.employee_table.setHorizontalHeaderLabels(["ID", "Фамилия", "Имя", "Дата Рождения", 
                                                         "Дата Приема", "Зарплата", "Email", 
                                                         "Телефон", "Фото", "ID Отдела", "ID Должности"])
    
        layout.addWidget(self.employee_table)

         # Вычисляемое поле для общей зарплаты
        self.total_salary_label = QLabel("Общая зарплата: 0")
        layout.addWidget(self.total_salary_label)

         # Установка основного макета
        self.setLayout(layout)


    def load_employees(self):
         """Загрузка данных о сотрудниках из базы данных"""
         
         # Очистка таблицы перед загрузкой данных
         self.employee_table.setRowCount(0)

         try:
             # Получение всех сотрудников из базы данных
             query = "SELECT * FROM employee"
             self.cursor.execute(query)
             employees = self.cursor.fetchall()

             for row in employees:
                 row_position = self.employee_table.rowCount()
                 self.employee_table.insertRow(row_position)
                 for column, data in enumerate(row):
                     item = QTableWidgetItem(str(data))
                     if column == 8:  # Фото
                         item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Запрет редактирования ячейки с фото
                     self.employee_table.setItem(row_position, column, item)

             QMessageBox.information(self, "Успех", "Данные о сотрудниках загружены.")

             # Вычисление общей зарплаты всех сотрудников
             total_salary_query = "SELECT SUM(salary) FROM employee"
             self.cursor.execute(total_salary_query)
             total_salary = self.cursor.fetchone()[0] or 0
             self.total_salary_label.setText(f"Общая зарплата: {total_salary}")

         except Exception as e:
             QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные: {e}")

    def validate_email(self, email):
         """Проверка корректности email"""
         
         regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
         
         return re.match(regex, email) is not None

    def validate_phone(self, phone):
         """Проверка корректности телефона"""
         
         return len(phone) == 11 and phone.isdigit()

    def add_employee(self):
         """Добавление нового сотрудника в базу данных"""
         
         id_text = self.id_input.text()
         surname = self.surname_input.text()
         name = self.name_input.text()
         birthday = self.birthday_input.text()
         date_of_employment = self.date_of_employment_input.text()
         salary_text = self.salary_input.text()
         email = self.email_input.text()
         phone = self.phone_input.text()
         id_department = self.id_department_input.text()
         id_position = self.id_position_input.text()

         if not id_text or not surname or not name or not birthday or not date_of_employment or not salary_text or not email or not phone or not id_department or not id_position:
             QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
             return

         if not (self.validate_email(email) and self.validate_phone(phone)):
             QMessageBox.warning(self, "Ошибка", "Неверный формат Email или телефона.")
             return

         try:
             salary = int(salary_text)  # Преобразуем зарплату в целое число

             if salary < 0 or salary > 10000000:
                 raise ValueError("Зарплата должна быть в диапазоне от 0 до 10 миллионов.")

             employee_id = int(id_text)  # Преобразуем ID сотрудника в целое число

             # Добавление нового сотрудника в базу данных
             query = """
                 INSERT INTO employee (id_employee, surname, name, birthday,
                 date_of_employment, salary, email, phone, id_department, id_position) VALUES (%s, %s, %s,
                 %s, %s, %s, %s, %s, %s, %s)
             """
             values = (employee_id, surname, name, birthday,
                       date_of_employment, salary, email,
                       phone, id_department, id_position)

             # Выполнение запроса на добавление
             self.cursor.execute(query, values)
             
             # Сохранение изменений
             self.cursor.connection.commit()
             QMessageBox.information(self, "Успех", "Сотрудник добавлен успешно!")
             self.load_employees()  # Обновление списка сотрудников

             # Очистка полей ввода
             for input_field in [self.id_input,
                                 self.surname_input,
                                 self.name_input,
                                 self.birthday_input,
                                 self.date_of_employment_input,
                                 self.salary_input,
                                 self.email_input,
                                 self.phone_input,
                                 self.id_department_input,
                                 self.id_position_input]:
                 input_field.clear()

         except Exception as e:
             QMessageBox.warning(self,"Ошибка", f"Не удалось добавить сотрудника: {e}")

    def update_employee(self):
          """Обновление информации о сотруднике""" 
          
          selected_row=self.employee_table.currentRow()

          if selected_row < 0:
              QMessageBox.warning(
                  None,
                  "Ошибка",
                  "Пожалуйста выберите сотрудника для обновления."
              )
              return

          old_employee_id_text=str(self.employee_table.item(selected_row , 0).text())

          new_id_text=self.id_input.text()
          surname=self.surname_input.text()
          name=self.name_input.text()
          birthday=self.birthday_input.text()
          date_of_employment=self.date_of_employment_input.text()
          salary_text=self.salary_input.text()
          email=self.email_input.text()
          phone=self.phone_input.text()
          new_id_department = self.id_department_input.text()
          new_id_position = self.id_position_input.text()

          if not new_id_text or not surname or not name or not birthday or not date_of_employment or not salary_text or not email or not phone:
              QMessageBox.warning(
                  None,
                  "Ошибка",
                  "Пожалуйста заполните все поля."
              )
              return

          if not (self.validate_email(email) and 
                   (self.validate_phone(phone))):
              QMessageBox.warning(
                  None,
                  "Ошибка",
                  "Неверный формат Email или телефона."
              )
              return 

          try:
              new_salary=int(salary_text) 

              if new_salary <0 or new_salary >10000000:
                  raise ValueError( )

              employee_id=int(new_id_text) 

              query= """
                  UPDATE employee SET id_employee=%s,surname=%s,name=%s,birthday=%s,date_of_employment=%s,salary=%s,email=%s,
                  phone=%s,id_department=%s,id_position=%s WHERE id_employee=%s
              """
              
              values=(employee_id,surname,name,birthday,date_of_employment,new_salary,email,phone,new_id_department,new_id_position,old_employee_id_text)

              self.cursor.execute(query ,values )
              
              self.cursor.connection.commit() 
              
              QMessageBox.information(
                  None,
                  "Успех",
                  "Сотрудник обновлен успешно!"
              )
              self.load_employees() 

          except Exception as e:
              QMessageBox.warning(
                  None,
                  "Ошибка",
                  f"Не удалось обновить сотрудника: {e}"
              )

    def delete_employee(self):
        selected_row = self.employee_table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(
                None,
                "Ошибка",
                "Пожалуйста выберите сотрудника для удаления."
            )
            return

        employee_id = int(self.employee_table.item(selected_row, 0).text())  # Получаем ID сотрудника из таблицы
    
        try:
            query = """
                DELETE FROM employee WHERE id_employee=%s
            """
        
            self.cursor.execute(query, (employee_id,))
            self.cursor.connection.commit()
        
            QMessageBox.information(
                None,
                "Успех",
                "Сотрудник удален успешно!"
            )
            self.load_employees()  # Обновляем список сотрудников

        except Exception as e:
            QMessageBox.warning(
                None,
                "Ошибка",
                f"Не удалось удалить сотрудника: {e}"
            )


    def upload_photo(self):
        """Загрузка фотографии сотрудника""" 
        selected_row = self.employee_table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(
                None,
                "Ошибка",
                "Пожалуйста выберите сотрудника для загрузки фото."
            )
            return 

        photo_path, _ = QFileDialog.getOpenFileName(self, "Выберите фото", "", "Images (*.png *.jpg *.jpeg *.bmp)")
    
        if photo_path:
            employee_id = int(self.employee_table.item(selected_row, 0).text())  # Получаем ID сотрудника
        
            query = """
                UPDATE employee SET photo=%s WHERE id_employee=%s
            """
        
            self.cursor.execute(query, (photo_path, employee_id))
            self.cursor.connection.commit() 
        
            QMessageBox.information(
                None,
                "Успех",
                "Фото загружено успешно!"
            )

            # Обновляем таблицу после загрузки фото
            self.load_employees()  # Это необходимо для обновления отображаемых данных


    def delete_photo(self):
        """Удаление фотографии сотрудника""" 
        selected_row = self.employee_table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(
                None,
                "Ошибка",
                "Пожалуйста выберите сотрудника для удаления фото."
            )
            return 

        employee_id = int(self.employee_table.item(selected_row, 0).text())  # Получаем ID сотрудника
    
        try:
            query = """
                UPDATE employee SET photo=NULL WHERE id_employee=%s
            """
        
            self.cursor.execute(query, (employee_id,))
            self.cursor.connection.commit() 
        
            QMessageBox.information(
                None,
                "Успех",
                "Фото удалено успешно!"
            )
        
            self.load_employees()  # Обновляем список сотрудников

        except Exception as e:
            QMessageBox.warning(
                None,
                "Ошибка",
                f"Не удалось удалить фото: {e}"
            )


    def show_photo_by_id(self):
          """Просмотр фотографии по ID""" 
          
          employee_id=self.id_input.text()

          try:
              query= """
                  SELECT photo FROM employee WHERE id_employee=%s
              """
              
              self.cursor.execute(query,(employee_id,))
              
              photo_path=self.cursor.fetchone()[0]
               
              pixmap=QPixmap(photo_path)
               
              label=QLabel()
              label.setPixmap(pixmap.scaled(200 ,200)) 
               
              label.show()

          except Exception as e:
                QMessageBox.warning(
                    None,
                    "Ошибка",
                    f"Не удалось загрузить фото: {e}"
                )

    def search_employee(self):
           """Поиск сотрудников по ФИО""" 
           
           search_term=self.search_input.text().strip().lower()

           if not search_term:
                QMessageBox.warning(
                    None,
                    "Ошибка",
                    "Введите поисковый запрос."
                )
                return 

           try:
                query= """
                    SELECT * FROM employee WHERE LOWER(surname) LIKE %s OR LOWER(name) LIKE %s
                """
                
                like_term=f"%{search_term}%"
                
                self.cursor.execute(query,(like_term ,like_term,))
                
                results=self.cursor.fetchall()

                # Очистка таблицы перед загрузкой результатов поиска
                self.employee_table.setRowCount(0)

                for row in results:
                    row_position=self.employee_table.rowCount()
                    self.employee_table.insertRow(row_position)
                    for column,data in enumerate(row):
                        item=QTableWidgetItem(str(data))
                        if column==8:  
                            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  
                        self.employee_table.setItem(row_position,column,item)

                if results:
                    QMessageBox.information(
                        None,
                        "Результаты поиска",
                        f"Найдено {len(results)} сотрудников."
                    )
                else:
                    QMessageBox.information(
                        None,
                        "Результаты поиска",
                        "Сотрудники не найдены."
                    )

           except Exception as e:
                QMessageBox.warning(
                    None,
                    "Ошибка",
                    f"Не удалось выполнить поиск: {e}"
                )

    def sort_employees(self):
           """Сортировка сотрудников по выбранному критерию""" 
           
           sort_criteria=self.sort_combo.currentText()

           if sort_criteria == "Сортировать по":
                QMessageBox.warning(
                    None,
                    "Ошибка",
                    "Выберите критерий сортировки."
                )
                return 

           try:
                 query=""
                 
                 if sort_criteria == "Фамилия":
                     query="SELECT * FROM employee ORDER BY surname"
                 elif sort_criteria == "Имя":
                     query="SELECT * FROM employee ORDER BY name"
                 elif sort_criteria == "Зарплата":
                     query="SELECT * FROM employee ORDER BY salary"

                 self.cursor.execute(query )   
                 results=self.cursor.fetchall()

                 self.employee_table.setRowCount(0)

                 for row in results:
                     row_position=self.employee_table.rowCount()
                     self.employee_table.insertRow(row_position )
                     for column,data in enumerate(row):
                         item=QTableWidgetItem(str(data))
                         if column==8:  
                             item.setFlags(item.flags() & ~Qt.ItemIsEditable)  
                         self.employee_table.setItem(row_position,column,item)


           except Exception as e:
                QMessageBox.warning(
                    None,
                    "Ошибка",
                    f"Не удалось выполнить сортировку: {e}"
                )

if __name__ == "__main__":
    app=QApplication(sys.argv)
    window=EmployeeManager(None)  
    window.show() 
    sys.exit(app.exec_())
