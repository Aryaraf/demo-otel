from flask import Flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Setup Flask
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# Setup OpenTelemetry Tracer
trace_provider = TracerProvider(
    resource = Resource.create({"service.name": "flask-app"})
)
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")  # ke Jaeger
span_processor = BatchSpanProcessor(otlp_exporter)
trace_provider.add_span_processor(span_processor)
from opentelemetry import trace
trace.set_tracer_provider(trace_provider)

@app.route("/")
def index():
    return "Hallo World!"

@app.route("/test")
def test():
    return "This is endpoint test."

if __name__ == "__main__":
    app.run(port=5000)
