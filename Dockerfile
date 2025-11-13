FROM python:3.13-slim

COPY requirements.txt .
COPY main.py .
COPY config_data.py .
COPY routes/ ./routes/
COPY helpers/ ./helpers/
COPY controllers/ ./controllers/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
