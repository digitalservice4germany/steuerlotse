import time

from fastapi import FastAPI
from prometheus_client import Gauge
from prometheus_fastapi_instrumentator import Instrumentator

from erica.pyeric.eric import verify_using_stick

app = FastAPI()


class DongleStatus:
    """
    Instrumentation helper to regularly check whether we still have a connection to the dongle.
    Caches results and only checks in fixed intervals to avoid performance penalties.
    """

    check_interval_in_seconds = 60
    last_checked = 0
    dongle_up_status = 1.0

    @classmethod
    def get(cls):
        now = time.time()
        if now - cls.last_checked > cls.check_interval_in_seconds:
            cls.dongle_up_status = 1.0 if verify_using_stick() else 0.0
            cls.last_checked = now

        return cls.dongle_up_status


# Add a metric from prometheus_client - these are automatically exported by the instrumentator.
up_metric = Gauge('up', 'Is the job available', ['job'])
up_metric.labels(job='erica').set(1.0)  # Always 1 when the erica_app is running.
up_metric.labels(job='dongle').set_function(DongleStatus.get)

# Add default metrics and expose endpoint.
Instrumentator().instrument(app).expose(app)

from erica import routes
