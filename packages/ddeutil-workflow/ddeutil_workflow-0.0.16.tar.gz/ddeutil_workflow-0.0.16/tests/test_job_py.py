from unittest import mock

import pytest
from ddeutil.workflow import Job, Workflow
from ddeutil.workflow.conf import Config
from ddeutil.workflow.exceptions import JobException
from ddeutil.workflow.utils import Result


def test_job_py():
    workflow: Workflow = Workflow.from_loader(
        name="wf-run-common", externals={}
    )
    job: Job = workflow.job("demo-run")

    # NOTE: Job params will change schema structure with {"params": { ... }}
    rs: Result = job.execute(params={"params": {"name": "Foo"}})
    assert {
        "1354680202": {
            "matrix": {},
            "stages": {
                "hello-world": {"outputs": {"x": "New Name"}},
                "run-var": {"outputs": {"x": 1}},
            },
        },
    } == rs.context


def test_job_py_raise():
    workflow: Workflow = Workflow.from_loader(
        name="wf-run-python-raise", externals={}
    )
    first_job: Job = workflow.job("first-job")

    with pytest.raises(JobException):
        first_job.execute(params={})


def test_job_py_not_set_output():
    with mock.patch.object(Config, "stage_default_id", False):
        # NOTE: Get stage from the specific workflow.
        workflow: Workflow = Workflow.from_loader(
            name="wf-run-python-raise", externals={}
        )
        job: Job = workflow.job("second-job")
        rs = job.execute(params={})
        assert {"1354680202": {"matrix": {}, "stages": {}}} == rs.context
