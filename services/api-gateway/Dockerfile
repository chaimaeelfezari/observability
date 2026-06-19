FROM python:3.11-slim
WORKDIR /app
RUN pip install flask requests \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp-proto-grpc \
    opentelemetry-instrumentation-flask \
    opentelemetry-instrumentation-requests
COPY app.py .
CMD ["python", "app.py"]