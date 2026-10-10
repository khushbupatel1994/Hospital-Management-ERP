FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements-server.txt requirements-phase8.txt ./
RUN pip install --no-cache-dir -r requirements-server.txt -r requirements-phase8.txt
COPY . .
RUN useradd --create-home --uid 10001 erp && chown -R erp:erp /app
USER erp
EXPOSE 8000
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
