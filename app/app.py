from prometheus_client import start_http_server, Counter, Gauge
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
import time, random

resource = Resource.create({"service.name": "python-app"})
provider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter(endpoint="http://tempo:4317", insecure=True)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

REQUESTS = Counter('app_requests_total', 'Total requests')
ACTIVE_USERS = Gauge('app_active_users', 'Active users')

if __name__ == '__main__':
    start_http_server(8000)
    print("App running on :8000")
    while True:
        with tracer.start_as_current_span("process_request"):
            REQUESTS.inc()
            ACTIVE_USERS.set(random.randint(1, 100))
            time.sleep(5)