# Используем официальный образ Python
   FROM python:3.9

   # Устанавливаем рабочую директорию
   WORKDIR /code

   # Копируем список зависимостей и устанавливаем их
   COPY requirements.txt /code/
   RUN pip install --no-cache-dir -r requirements.txt

   # Копируем весь проект в контейнер
   COPY . /code/

   # Expose port 8000
   EXPOSE 8000

   # Команда для запуска сервера Django
   CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
