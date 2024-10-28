"""
    Easy logging wrapper for cosmicfrog library, supports Insights logging if available
"""
import logging
import os
import sys
from logging import Logger

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

app_logger = {}


def get_logger(console_only: bool = False) -> Logger:
    """
    Gets an appropriate Logger instance (configured, connected to Azure Monitor if available)
    """
    current_pid = str(os.getpid())

    if current_pid in app_logger:
        return app_logger[current_pid]

    log_level = os.getenv("FROG_LOG_LEVEL") or logging.DEBUG
    log_level = int(log_level)

    logger = logging.getLogger(current_pid)
    app_logger[current_pid] = logger

    # Add log to Azure Monitor (OL internal only)
    if not console_only:
        insights_connection = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

        if insights_connection:
            # Set up OpenTelemetry for Azure Monitor
            resource = Resource.create({"service.name": "cosmicfrog"})
            provider = TracerProvider(resource=resource)
            trace.set_tracer_provider(provider)

            exporter = AzureMonitorTraceExporter(connection_string=insights_connection)
            span_processor = BatchSpanProcessor(exporter)
            provider.add_span_processor(span_processor)

            # You can log traces or use logger as needed
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span("cosmicfrog_logging"):
                logger.info("Azure Monitor logging is configured")

    # Add log to console
    stdhandler = logging.StreamHandler(sys.stdout)
    stdhandler.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stdhandler.setFormatter(formatter)
    logger.addHandler(stdhandler)

    logger.setLevel(log_level)

    return logger
