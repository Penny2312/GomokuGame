# python:3.8-slim  wordt als basisimage gebruikt
FROM python:3.8-slim

# Werkdirectory instellen
WORKDIR /app

# Afhankelijkheden installeren
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Broncode kopiëren
COPY . .

# De Flask-app starten
CMD ["python", "app.py"]
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]