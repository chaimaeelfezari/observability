FROM python:3.11-slim
WORKDIR /app
RUN pip install prometheus-client==0.20.0 opentelemetry-sdk==1.25.0 opentelemetry-exporter-otlp-proto-grpc==1.25.0
COPY app.py .
EXPOSE 8000
CMD ["python", "app.py"]