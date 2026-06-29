FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi>=0.110 uvicorn>=0.29
COPY demo_repo ./demo_repo
COPY shop-api ./shop-api
EXPOSE 8080
CMD ["python", "-m", "uvicorn", "app:app", "--app-dir", "shop-api", "--host", "0.0.0.0", "--port", "8080"]
