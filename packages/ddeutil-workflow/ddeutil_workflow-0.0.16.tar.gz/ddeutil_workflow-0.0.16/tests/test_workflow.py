import pytest
from ddeutil.workflow import Job, Workflow
from ddeutil.workflow.utils import Result
from pydantic import ValidationError


def test_workflow_model():
    data = {
        "demo-run": {
            "stages": [
                {"name": "Run Hello World", "run": "print(f'Hello {x}')\n"},
                {
                    "name": "Run Sequence and use var from Above",
                    "run": (
                        "print(f'Receive x from above with {x}')\n\n"
                        "x: int = 1\n"
                    ),
                },
            ]
        },
        "next-run": {
            "stages": [
                {
                    "name": "Set variable and function",
                    "run": (
                        "var_inside: str = 'Inside'\n"
                        "def echo() -> None:\n"
                        '  print(f"Echo {var_inside}"\n'
                    ),
                },
                {"name": "Call that variable", "run": "echo()\n"},
            ]
        },
    }
    p = Workflow(name="manual-workflow", jobs=data)
    assert "Run Hello World" == p.jobs.get("demo-run").stages[0].name
    assert (
        "Run Sequence and use var from Above"
        == p.jobs.get("demo-run").stages[1].name
    )

    demo_job: Job = p.job("demo-run")
    assert [{}] == demo_job.strategy.make()


def test_workflow_model_name_raise():

    with pytest.raises(ValidationError):
        Workflow(name="manual-workflow-${{ params.test }}")


def test_workflow_desc():
    workflow = Workflow.from_loader(
        name="wf-run-common",
        externals={},
    )
    assert workflow.desc == (
        "## Run Python Workflow\n\nThis is a running python workflow\n"
    )


def test_workflow_condition():
    workflow = Workflow.from_loader(name="wf-condition", externals={})
    rs: Result = workflow.execute(params={"name": "bar"})
    assert {
        "params": {"name": "bar"},
        "jobs": {
            "condition-job": {
                "matrix": {},
                "stages": {
                    "6708019737": {"outputs": {}},
                },
            },
        },
    } == rs.context
