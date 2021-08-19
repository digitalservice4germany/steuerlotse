import json

# cf. https://github.com/rycus86/prometheus_flask_exporter/tree/master/examples/gunicorn-internal
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics


def child_exit(server, worker):
    GunicornInternalPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)


with open('logging.json') as f:
    logconfig_dict = json.load(f)


workers = 4
bind = '0.0.0.0:5000'
worker_tmp_dir = '/tmp'
# See https://docs.gunicorn.org/en/stable/settings.html#access-log-format
access_log_format = '%({x-request-id}i)s %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
