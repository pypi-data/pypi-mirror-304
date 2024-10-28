import ddeutil.workflow as wf


def test_workflow_strategy_model():
    strategy = wf.Strategy.model_validate(
        obj={
            "matrix": {
                "table": ["customer", "sales"],
                "system": ["csv"],
                "partition": [1, 2, 3],
            },
            "exclude": [
                {
                    "table": "customer",
                    "system": "csv",
                    "partition": 1,
                },
                {
                    "table": "sales",
                    "partition": 3,
                },
            ],
            "include": [
                {
                    "table": "customer",
                    "system": "csv",
                    "partition": 4,
                }
            ],
        }
    )
    assert sorted(
        [
            {"partition": 1, "system": "csv", "table": "sales"},
            {"partition": 2, "system": "csv", "table": "customer"},
            {"partition": 2, "system": "csv", "table": "sales"},
            {"partition": 3, "system": "csv", "table": "customer"},
            {"partition": 4, "system": "csv", "table": "customer"},
        ],
        key=lambda x: (x["partition"], x["table"]),
    ) == sorted(
        strategy.make(),
        key=lambda x: (x["partition"], x["table"]),
    )


def test_workflow_job_matrix():
    workflow = wf.Workflow.from_loader(
        name="wf-run-matrix",
        externals={},
    )
    multi_sys = workflow.job(name="multiple-system")
    assert {
        "system": ["csv"],
        "table": ["customer", "sales"],
        "partition": [1, 2, 3],
    } == multi_sys.strategy.matrix
    assert 1 == multi_sys.strategy.max_parallel
    assert [
        {"partition": 4, "system": "csv", "table": "customer"},
    ] == multi_sys.strategy.include
    assert [
        {"table": "customer", "system": "csv", "partition": 1},
        {"table": "sales", "partition": 3},
    ] == multi_sys.strategy.exclude
    assert sorted(
        [
            {"partition": 1, "system": "csv", "table": "sales"},
            {"partition": 2, "system": "csv", "table": "customer"},
            {"partition": 2, "system": "csv", "table": "sales"},
            {"partition": 3, "system": "csv", "table": "customer"},
            {"partition": 4, "system": "csv", "table": "customer"},
        ],
        key=lambda x: (x["partition"], x["table"]),
    ) == sorted(
        multi_sys.strategy.make(),
        key=lambda x: (x["partition"], x["table"]),
    )


def test_workflow_matrix():
    workflow = wf.Workflow.from_loader(name="wf-run-matrix")
    rs = workflow.execute(params={"source": "src", "target": "tgt"})
    assert {
        "params": {"source": "src", "target": "tgt"},
        "jobs": {
            "multiple-system": {
                "strategies": {
                    "9696245497": {
                        "matrix": {
                            "table": "customer",
                            "system": "csv",
                            "partition": 2,
                        },
                        "stages": {
                            "customer-2": {"outputs": {"records": 1}},
                            "end-stage": {"outputs": {"passing_value": 10}},
                        },
                    },
                    "8141249744": {
                        "matrix": {
                            "table": "customer",
                            "system": "csv",
                            "partition": 3,
                        },
                        "stages": {
                            "customer-3": {"outputs": {"records": 1}},
                            "end-stage": {"outputs": {"passing_value": 10}},
                        },
                    },
                    "3590257855": {
                        "matrix": {
                            "table": "sales",
                            "system": "csv",
                            "partition": 1,
                        },
                        "stages": {
                            "sales-1": {"outputs": {"records": 1}},
                            "end-stage": {"outputs": {"passing_value": 10}},
                        },
                    },
                    "3698996074": {
                        "matrix": {
                            "table": "sales",
                            "system": "csv",
                            "partition": 2,
                        },
                        "stages": {
                            "sales-2": {"outputs": {"records": 1}},
                            "end-stage": {"outputs": {"passing_value": 10}},
                        },
                    },
                    "4390593385": {
                        "matrix": {
                            "table": "customer",
                            "system": "csv",
                            "partition": 4,
                        },
                        "stages": {
                            "customer-4": {"outputs": {"records": 1}},
                            "end-stage": {"outputs": {"passing_value": 10}},
                        },
                    },
                },
            },
        },
    } == rs.context


def test_workflow_matrix_fail_fast():
    workflow = wf.Workflow.from_loader(
        name="wf-run-matrix-fail-fast",
        externals={},
    )
    rs = workflow.execute(params={"name": "foo"})
    print(rs)
