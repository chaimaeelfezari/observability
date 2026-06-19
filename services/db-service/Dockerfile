FROM python:3.11-slim
WORKDIR /app
RUN pip install flask \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp-proto-grpc \
    opentelemetry-instrumentation-flask
COPY app.py .
CMD ["python", "app.py"]