from prometheus_client import start_http_server, Counter, Gauge
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
import time, random, logging

resource = Resource.create({"service.name": "python-app"})

# Traces
provider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# Logs
logger_provider = LoggerProvider(resource=resource)
log_exporter = OTLPLogExporter(endpoint="http://otel-collector:4317", insecure=True)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
set_logger_provider(logger_provider)
handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

REQUESTS = Counter('app_requests_total', 'Total requests')
ACTIVE_USERS = Gauge('app_active_users', 'Active users')

if __name__ == '__main__':
    start_http_server(8000)
    logging.info("App running on :8000")
    while True:
        with tracer.start_as_current_span("process_request"):
            REQUESTS.inc()
            users = random.randint(1, 100)
            ACTIVE_USERS.set(users)
            logging.info(f"Processed request, active_users={users}")
            time.sleep(5)