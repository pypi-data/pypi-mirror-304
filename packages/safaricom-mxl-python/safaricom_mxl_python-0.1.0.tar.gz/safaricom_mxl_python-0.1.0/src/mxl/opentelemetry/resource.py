import platform
from opentelemetry.sdk.resources import Resource
from mxl.opentelemetry.options import MXLOptions
from mxl.opentelemetry.version import __version__


def create_resource(options: MXLOptions):
    """
    Configures and returns a new OpenTelemetry Resource.

    Args:
        options (MXLOptions): the MXL options to configure with
        resource (Resource): the resource to use with the new resource

    Returns:
        MeterProvider: the new Resource
    """
    attributes = {
        "service.name": options.service_name,
        "mxl.distro.version": __version__,
        "mxl.distro.runtime_version": platform.python_version()
    }
    if options.service_version:
        attributes["service.version"] = options.service_version
    return Resource.create(attributes)
