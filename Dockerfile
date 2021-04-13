FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY requirements.txt /tmp
WORKDIR /tmp
RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 7100
WORKDIR /app/
CMD ["uvicorn", "main:app", "--reload", "--port", "7100", "--host", "0.0.0.0", "--workers", "5"]