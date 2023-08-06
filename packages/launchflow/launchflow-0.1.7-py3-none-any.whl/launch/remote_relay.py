import os
import signal
import subprocess
from sys import platform
from dataclasses import dataclass
from pkg_resources import resource_filename
from typing import Dict

import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ray.job_submission import JobSubmissionClient

RAY_CLUSTER_ADDRESS = 'http://127.0.0.1:8265'
PROMETHEUS = 'http://localhost:9090/'


@dataclass
class JobInfo:
    job_id: str
    status: str
    metrics: Dict[str, str]


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event("startup")
def startup():
    prom_dir = resource_filename('launch', 'prometheus')
    if platform == "linux" or platform == "linux2":
        executable = 'linux/prometheus'
    elif platform == "darwin":
        executable = 'mac/prometheus'
    else:
        raise ValueError(
            f'launch CLI is not supported for platform: {platform}')
    subprocess.Popen(
        f'./{executable} --config.file=/tmp/ray/session_latest/metrics/prometheus/prometheus.yml',  # noqa
        cwd=f'{prom_dir}/.',
        shell=True)


def get_prometheus_metrics(metric, fn):
    query = f'ray_{metric}'
    if fn is not None:
        query = f'{fn}({query})'
    response = requests.get(PROMETHEUS + '/api/v1/query',
                            params={
                                'query': query
                            }).json()
    if response.get('status') == 'success':
        try:
            return response.get('data').get('result')[0].get('value')[1]
        except Exception:
            return None


@app.get('/get_job')
async def get_job(job_id: str):
    client = JobSubmissionClient(RAY_CLUSTER_ADDRESS)
    job_info = client.get_job_info(job_id)
    job_info.metadata['throughput'] = 'N/A'
    job_info.metadata['num_replicas'] = 'N/A'
    job_info.metadata['process_time'] = 'N/A'
    for metric, fn in [('num_replicas', None), ('process_time', 'avg'),
                       ('throughput', 'sum')]:
        prom_metric = get_prometheus_metrics(metric, fn)
        if prom_metric is not None:
            job_info.metadata[metric] = prom_metric
    return job_info


@app.get('/drain_job')
async def drain_job(job_id: str):
    client = JobSubmissionClient(RAY_CLUSTER_ADDRESS)
    job_info = client.get_job_info(job_id)
    pid = job_info.driver_info.pid
    os.kill(int(pid), signal.SIGTERM)
    return True
