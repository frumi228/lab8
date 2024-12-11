
FROM python:3.10-slim


WORKDIR /app


COPY requirements.txt /app/


RUN pip install --upgrade pip && pip install -r requirements.txt


COPY . /app/


ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH=/app

# Запускаємо серв
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
