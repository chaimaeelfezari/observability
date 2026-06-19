from prometheus_client import start_http_server, Counter, Gauge, Histogram
from prometheus_client import exposition
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

# Histogram avec exemplars — lie chaque mesure à un trace_id Tempo
REQUEST_LATENCY = Histogram(
    'app_request_duration_seconds',
    'Request latency with exemplars',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

def get_trace_id():
    """Retourne le trace_id du span courant pour l'exemplar."""
    ctx = trace.get_current_span().get_span_context()
    if ctx and ctx.is_valid:
        return format(ctx.trace_id, '032x')
    return None

if __name__ == '__main__':
    start_http_server(8000)
    logging.info("App running on :8000")
    while True:
        with tracer.start_as_current_span("process_request") as span:
            start = time.time()

            REQUESTS.inc()
            users = random.randint(1, 100)
            ACTIVE_USERS.set(users)

            # Simuler latence variable (parfois lente pour voir dans Grafana)
            latency = random.choice([0.1, 0.2, 0.5, 1.0, 2.0, 4.0])
            time.sleep(latency)

            duration = time.time() - start
            trace_id = get_trace_id()

            # Ajouter exemplar : lie la métrique → trace Tempo
            if trace_id:
                REQUEST_LATENCY.observe(duration, exemplar={"traceID": trace_id})
            else:
                REQUEST_LATENCY.observe(duration)

            span.set_attribute("active_users", users)
            span.set_attribute("latency_seconds", duration)
            logging.info(f"Processed request, active_users={users}, latency={duration:.2f}s, trace_id={trace_id}")