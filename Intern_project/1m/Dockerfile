FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY btcloader_1m_futures.py /app/
COPY schemas.py /app/

CMD ["python","btcloader_1m_futures.py"]
