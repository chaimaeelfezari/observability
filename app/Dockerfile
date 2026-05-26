FROM python:3.11-slim
RUN pip install prometheus-client opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc
COPY app.py .
CMD ["python", "app.py"]