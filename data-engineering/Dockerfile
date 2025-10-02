FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dataset.py pipeline_preprocessing.py ./

CMD ["python", "pipeline_preprocessing.py"]
