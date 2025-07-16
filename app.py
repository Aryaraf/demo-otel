from flask import Flask
from flask import request
import time
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "flask-app"}),
    )
)
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")  
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/test")
def test():
    return "This is endpoint test."

@app.route("/span")
def span():
    with trace.get_tracer(__name__).start_as_current_span("simulated-processing") as span:
        span.set_attribute("user.id", "1234")
        span.set_attribute("opertaion.type", "simulated-task")
        span.set_attribute("status", "running")
        time.sleep(1)
    return "Span with attribute has been sent"

if __name__ == "__main__":
    app.run(port=5000)
