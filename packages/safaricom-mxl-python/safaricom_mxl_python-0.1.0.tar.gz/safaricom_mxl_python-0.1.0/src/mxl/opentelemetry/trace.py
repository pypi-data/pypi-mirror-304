from opentelemetry.processor.baggage import (
    ALLOW_ALL_BAGGAGE_KEYS,
    BaggageSpanProcessor
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SimpleSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as GRPCSpanExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as HTTPSpanExporter,
)

from mxl.opentelemetry.options import MXLOptions
from mxl.opentelemetry.sampler import configure_sampler


def create_tracer_provider(
    options: MXLOptions, resource: Resource
) -> TracerProvider:
    """
    Configures and returns a new TracerProvider to send traces telemetry.

    Args:
        options (MXLOptions): the MXL options to configure with
        resource (Resource): the resource to use with the new tracer provider

    Returns:
        TracerProvider: the new tracer provider
    """
    if options.traces_exporter_protocol == "grpc":
        exporter = GRPCSpanExporter(
            endpoint=options.get_traces_endpoint(),
            credentials=options.get_trace_endpoint_credentials(),
            headers=options.get_trace_headers(),
        )
    else:
        exporter = HTTPSpanExporter(
            endpoint=options.get_traces_endpoint(), headers=options.get_trace_headers()
        )
    trace_provider = TracerProvider(
        resource=resource, sampler=configure_sampler(options)
    )
    trace_provider.add_span_processor(
        BaggageSpanProcessor(ALLOW_ALL_BAGGAGE_KEYS)
    )

    trace_provider.add_span_processor(BatchSpanProcessor(exporter))
    if options.debug:
        trace_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    return trace_provider
