# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
"""Stage Model that use for getting stage data template from the Job Model.
The stage handle the minimize task that run in some thread (same thread at
its job owner) that mean it is the lowest executor of a workflow workflow that
can tracking logs.

    The output of stage execution only return 0 status because I do not want to
handle stage error on this stage model. I think stage model should have a lot of
usecase and it does not worry when I want to create a new one.

    Execution   --> Ok      --> Result with 0
                --> Error   --> Raise StageException
                            --> Result with 1 (if env var was set)

    On the context I/O that pass to a stage object at execute process. The
execute method receives a `params={"params": {...}}` value for mapping to
template searching.
"""
from __future__ import annotations

import contextlib
import inspect
import subprocess
import sys
import time
import uuid
from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass
from functools import wraps
from inspect import Parameter
from pathlib import Path
from subprocess import CompletedProcess
from textwrap import dedent
from typing import Callable, Optional, Union

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

from pydantic import BaseModel, Field
from pydantic.functional_validators import model_validator
from typing_extensions import Self

from .__types import DictData, DictStr, Re, TupleStr
from .conf import config
from .exceptions import StageException
from .log import get_logger
from .utils import (
    Registry,
    Result,
    TagFunc,
    gen_id,
    make_exec,
    make_registry,
    not_in_template,
    param2template,
)

P = ParamSpec("P")
ReturnResult = Callable[P, Result]
DecoratorResult = Callable[[ReturnResult], ReturnResult]
logger = get_logger("ddeutil.workflow")


__all__: TupleStr = (
    "BaseStage",
    "EmptyStage",
    "BashStage",
    "PyStage",
    "HookStage",
    "TriggerStage",
    "Stage",
    "HookSearchData",
    "extract_hook",
    "handler_result",
)


def handler_result(message: str | None = None) -> DecoratorResult:
    """Decorator function for handler result from the stage execution. This
    function should to use with execution method only.

        This stage exception handler still use ok-error concept but it allow
    you force catching an output result with error message by specific
    environment variable,`WORKFLOW_CORE_STAGE_RAISE_ERROR`.

        Execution   --> Ok      --> Result
                                        status: 0
                                        context:
                                            outputs: ...
                    --> Error   --> Raise StageException
                                --> Result (if env var was set)
                                        status: 1
                                        context:
                                            error: ...
                                            error_message: ...

        On the last step, it will set the running ID on a return result object
    from current stage ID before release the final result.

    :param message: A message that want to add at prefix of exception statement.
    :type message: str | None (Default=None)
    :rtype: Callable[P, Result]
    """
    # NOTE: The prefix message string that want to add on the first exception
    #   message dialog.
    #
    #       >>> ValueError: {message}
    #       ...     raise value error from the stage execution process.
    #
    message: str = message or ""

    def decorator(func: ReturnResult) -> ReturnResult:

        @wraps(func)
        def wrapped(self: Stage, *args, **kwargs):
            try:
                # NOTE: Start calling origin function with a passing args.
                return func(self, *args, **kwargs).set_run_id(self.run_id)
            except Exception as err:
                # NOTE: Start catching error from the stage execution.
                logger.error(
                    f"({self.run_id}) [STAGE]: {err.__class__.__name__}: {err}"
                )
                if config.stage_raise_error:
                    # NOTE: If error that raise from stage execution course by
                    #   itself, it will return that error with previous
                    #   dependency.
                    if isinstance(err, StageException):
                        raise StageException(
                            f"{self.__class__.__name__}: {message}\n\t{err}"
                        ) from err
                    raise StageException(
                        f"{self.__class__.__name__}: {message}\n\t"
                        f"{err.__class__.__name__}: {err}"
                    ) from None

                # NOTE: Catching exception error object to result with
                #   error_message and error keys.
                return Result(
                    status=1,
                    context={
                        "error": err,
                        "error_message": f"{err.__class__.__name__}: {err}",
                    },
                ).set_run_id(self.run_id)

        return wrapped

    return decorator


class BaseStage(BaseModel, ABC):
    """Base Stage Model that keep only id and name fields for the stage
    metadata. If you want to implement any custom stage, you can use this class
    to parent and implement ``self.execute()`` method only.
    """

    id: Optional[str] = Field(
        default=None,
        description=(
            "A stage ID that use to keep execution output or getting by job "
            "owner."
        ),
    )
    name: str = Field(
        description="A stage name that want to logging when start execution.",
    )
    condition: Optional[str] = Field(
        default=None,
        description="A stage condition statement to allow stage executable.",
        alias="if",
    )
    run_id: Optional[str] = Field(
        default=None,
        description="A running stage ID.",
        repr=False,
        exclude=True,
    )

    @model_validator(mode="after")
    def __prepare_running_id__(self) -> Self:
        """Prepare stage running ID that use default value of field and this
        method will validate name and id fields should not contain any template
        parameter (exclude matrix template).

        :rtype: Self
        """
        if self.run_id is None:
            self.run_id = gen_id(self.name + (self.id or ""), unique=True)

        # VALIDATE: Validate stage id and name should not dynamic with params
        #   template. (allow only matrix)
        if not_in_template(self.id) or not_in_template(self.name):
            raise ValueError(
                "Stage name and ID should only template with matrix."
            )

        return self

    def get_running_id(self, run_id: str) -> Self:
        """Return Stage model object that changing stage running ID with an
        input running ID.

        :param run_id: A replace stage running ID.
        :rtype: Self
        """
        return self.model_copy(update={"run_id": run_id})

    @abstractmethod
    def execute(self, params: DictData) -> Result:
        """Execute abstraction method that action something by sub-model class.
        This is important method that make this class is able to be the stage.

        :param params: A parameter data that want to use in this execution.
        :rtype: Result
        """
        raise NotImplementedError("Stage should implement ``execute`` method.")

    def set_outputs(self, output: DictData, to: DictData) -> DictData:
        """Set an outputs from execution process to the receive context. The
        result from execution will pass to value of ``outputs`` key.

            For example of setting output method, If you receive execute output
        and want to set on the `to` like;

            ... (i)   output: {'foo': bar}
            ... (ii)  to: {}

        The result of the `to` variable will be;

            ... (iii) to: {
                            'stages': {
                                '<stage-id>': {'outputs': {'foo': 'bar'}}
                            }
                        }

        :param output: A output data that want to extract to an output key.
        :param to: A context data that want to add output result.
        :rtype: DictData
        """
        if self.id is None and not config.stage_default_id:
            logger.debug(
                f"({self.run_id}) [STAGE]: Output does not set because this "
                f"stage does not set ID or default stage ID config flag not be "
                f"True."
            )
            return to

        # NOTE: Create stages key to receive an output from the stage execution.
        if "stages" not in to:
            to["stages"] = {}

        # NOTE: If the stage ID did not set, it will use its name instead.
        _id: str = (
            param2template(self.id, params=to)
            if self.id
            else gen_id(param2template(self.name, params=to))
        )

        # NOTE: Set the output to that stage generated ID with ``outputs`` key.
        logger.debug(f"({self.run_id}) [STAGE]: Set outputs to {_id!r}")
        to["stages"][_id] = {"outputs": output}
        return to

    def is_skipped(self, params: DictData | None = None) -> bool:
        """Return true if condition of this stage do not correct. This process
        use build-in eval function to execute the if-condition.

        :param params: A parameters that want to pass to condition template.
        :rtype: bool
        """
        if self.condition is None:
            return False

        params: DictData = {} if params is None else params
        _g: DictData = globals() | params
        try:
            rs: bool = eval(param2template(self.condition, params), _g, {})
            if not isinstance(rs, bool):
                raise TypeError("Return type of condition does not be boolean")
            return not rs
        except Exception as err:
            logger.error(f"({self.run_id}) [STAGE]: {err}")
            raise StageException(f"{err.__class__.__name__}: {err}") from err


class EmptyStage(BaseStage):
    """Empty stage that do nothing (context equal empty stage) and logging the
    name of stage only to stdout.

    Data Validate:
        >>> stage = {
        ...     "name": "Empty stage execution",
        ...     "echo": "Hello World",
        ... }
    """

    echo: Optional[str] = Field(
        default=None,
        description="A string statement that want to logging",
    )
    sleep: float = Field(
        default=0,
        description="A second value to sleep before finish execution",
        ge=0,
    )

    def execute(self, params: DictData) -> Result:
        """Execution method for the Empty stage that do only logging out to
        stdout. This method does not use the `handler_result` decorator because
        it does not get any error from logging function.

            The result context should be empty and do not process anything
        without calling logging function.

        :param params: A context data that want to add output result. But this
            stage does not pass any output.
        :rtype: Result
        """
        logger.info(
            f"({self.run_id}) [STAGE]: Empty-Execute: {self.name!r}: "
            f"( {param2template(self.echo, params=params) or '...'} )"
        )
        if self.sleep > 0:
            time.sleep(self.sleep)
        return Result(status=0, context={})


class BashStage(BaseStage):
    """Bash execution stage that execute bash script on the current OS.
    That mean if your current OS is Windows, it will running bash in the WSL.

        I get some limitation when I run shell statement with the built-in
    supprocess package. It does not good enough to use multiline statement.
    Thus, I add writing ``.sh`` file before execution process for fix this
    issue.

    Data Validate:
        >>> stage = {
        ...     "name": "Shell stage execution",
        ...     "bash": 'echo "Hello $FOO"',
        ...     "env": {
        ...         "FOO": "BAR",
        ...     },
        ... }
    """

    bash: str = Field(description="A bash statement that want to execute.")
    env: DictStr = Field(
        default_factory=dict,
        description=(
            "An environment variable mapping that want to set before execute "
            "this shell statement."
        ),
    )

    @contextlib.contextmanager
    def prepare_bash(self, bash: str, env: DictStr) -> Iterator[TupleStr]:
        """Return context of prepared bash statement that want to execute. This
        step will write the `.sh` file before giving this file name to context.
        After that, it will auto delete this file automatic.

        :param bash: A bash statement that want to execute.
        :param env: An environment variable that use on this bash statement.
        :rtype: Iterator[TupleStr]
        """
        f_name: str = f"{uuid.uuid4()}.sh"
        f_shebang: str = "bash" if sys.platform.startswith("win") else "sh"
        with open(f"./{f_name}", mode="w", newline="\n") as f:
            # NOTE: write header of `.sh` file
            f.write(f"#!/bin/{f_shebang}\n\n")

            # NOTE: add setting environment variable before bash skip statement.
            f.writelines([f"{k}='{env[k]}';\n" for k in env])

            # NOTE: make sure that shell script file does not have `\r` char.
            f.write("\n" + bash.replace("\r\n", "\n"))

        # NOTE: Make this .sh file able to executable.
        make_exec(f"./{f_name}")

        logger.debug(
            f"({self.run_id}) [STAGE]: Start create `.sh` file and running a "
            f"bash statement."
        )

        yield [f_shebang, f_name]

        # Note: Remove .sh file that use to run bash.
        Path(f"./{f_name}").unlink()

    @handler_result()
    def execute(self, params: DictData) -> Result:
        """Execute the Bash statement with the Python build-in ``subprocess``
        package.

        :param params: A parameter data that want to use in this execution.
        :rtype: Result
        """
        bash: str = param2template(dedent(self.bash), params)
        with self.prepare_bash(
            bash=bash, env=param2template(self.env, params)
        ) as sh:
            logger.info(f"({self.run_id}) [STAGE]: Shell-Execute: {sh}")
            rs: CompletedProcess = subprocess.run(
                sh, shell=False, capture_output=True, text=True
            )
        if rs.returncode > 0:
            # NOTE: Prepare stderr message that returning from subprocess.
            err: str = (
                rs.stderr.encode("utf-8").decode("utf-16")
                if "\\x00" in rs.stderr
                else rs.stderr
            ).removesuffix("\n")
            raise StageException(
                f"Subprocess: {err}\nRunning Statement:\n---\n"
                f"```bash\n{bash}\n```"
            )
        return Result(
            status=0,
            context={
                "return_code": rs.returncode,
                "stdout": rs.stdout.rstrip("\n") or None,
                "stderr": rs.stderr.rstrip("\n") or None,
            },
        )


class PyStage(BaseStage):
    """Python executor stage that running the Python statement with receiving
    globals and additional variables.

        This stage allow you to use any Python object that exists on the globals
    such as import your installed package.

    Data Validate:
        >>> stage = {
        ...     "name": "Python stage execution",
        ...     "run": 'print("Hello {x}")',
        ...     "vars": {
        ...         "x": "BAR",
        ...     },
        ... }
    """

    run: str = Field(
        description="A Python string statement that want to run with exec.",
    )
    vars: DictData = Field(
        default_factory=dict,
        description=(
            "A mapping to variable that want to pass to globals in exec."
        ),
    )

    def set_outputs(self, output: DictData, to: DictData) -> DictData:
        """Override set an outputs method for the Python execution process that
        extract output from all the locals values.

        :param output: A output data that want to extract to an output key.
        :param to: A context data that want to add output result.
        :rtype: DictData
        """
        # NOTE: The output will fileter unnecessary keys from locals.
        _locals: DictData = output["locals"]
        super().set_outputs(
            {k: _locals[k] for k in _locals if k != "__annotations__"}, to=to
        )

        # NOTE:
        #   Override value that changing from the globals that pass via exec.
        _globals: DictData = output["globals"]
        to.update({k: _globals[k] for k in to if k in _globals})
        return to

    @handler_result()
    def execute(self, params: DictData) -> Result:
        """Execute the Python statement that pass all globals and input params
        to globals argument on ``exec`` build-in function.

        :param params: A parameter that want to pass before run any statement.
        :rtype: Result
        """
        # NOTE: Replace the run statement that has templating value.
        run: str = param2template(dedent(self.run), params)

        # NOTE: create custom globals value that will pass to exec function.
        _globals: DictData = (
            globals() | params | param2template(self.vars, params)
        )
        _locals: DictData = {}

        # NOTE: Start exec the run statement.
        logger.info(f"({self.run_id}) [STAGE]: Py-Execute: {self.name}")
        exec(run, _globals, _locals)

        return Result(
            status=0,
            context={"locals": _locals, "globals": _globals},
        )


@dataclass(frozen=True)
class HookSearchData:
    """Hook Search dataclass that use for receive regular expression grouping
    dict from searching hook string value.
    """

    path: str
    func: str
    tag: str


def extract_hook(hook: str) -> Callable[[], TagFunc]:
    """Extract Hook function from string value to hook partial function that
    does run it at runtime.

    :param hook: A hook value that able to match with Task regex.
    :rtype: Callable[[], TagFunc]
    """
    if not (found := Re.RE_TASK_FMT.search(hook)):
        raise ValueError(
            f"Hook {hook!r} does not match with hook format regex."
        )

    # NOTE: Pass the searching hook string to `path`, `func`, and `tag`.
    hook: HookSearchData = HookSearchData(**found.groupdict())

    # NOTE: Registry object should implement on this package only.
    rgt: dict[str, Registry] = make_registry(f"{hook.path}")
    if hook.func not in rgt:
        raise NotImplementedError(
            f"``REGISTER-MODULES.{hook.path}.registries`` does not "
            f"implement registry: {hook.func!r}."
        )

    if hook.tag not in rgt[hook.func]:
        raise NotImplementedError(
            f"tag: {hook.tag!r} does not found on registry func: "
            f"``REGISTER-MODULES.{hook.path}.registries.{hook.func}``"
        )
    return rgt[hook.func][hook.tag]


class HookStage(BaseStage):
    """Hook executor that hook the Python function from registry with tag
    decorator function in ``utils`` module and run it with input arguments.

        This stage is different with PyStage because the PyStage is just calling
    a Python statement with the ``eval`` and pass that locale before eval that
    statement. So, you can create your function complexly that you can for your
    propose to invoked by this stage object.

    Data Validate:
        >>> stage = {
        ...     "name": "Task stage execution",
        ...     "uses": "tasks/function-name@tag-name",
        ...     "args": {"FOO": "BAR"},
        ... }
    """

    uses: str = Field(
        description=(
            "A pointer that want to load function from the hook registry."
        ),
    )
    args: DictData = Field(
        default_factory=dict,
        description="An arguments that want to pass to the hook function.",
        alias="with",
    )

    @handler_result()
    def execute(self, params: DictData) -> Result:
        """Execute the Hook function that already in the hook registry.

        :param params: A parameter that want to pass before run any statement.
        :type params: DictData
        :rtype: Result
        """
        t_func_hook: str = param2template(self.uses, params)
        t_func: TagFunc = extract_hook(t_func_hook)()

        # VALIDATE: check input task caller parameters that exists before
        #   calling.
        args: DictData = param2template(self.args, params)
        ips = inspect.signature(t_func)
        if any(
            (k.removeprefix("_") not in args and k not in args)
            for k in ips.parameters
            if ips.parameters[k].default == Parameter.empty
        ):
            raise ValueError(
                f"Necessary params, ({', '.join(ips.parameters.keys())}, ), "
                f"does not set to args"
            )
        # NOTE: add '_' prefix if it want to use.
        for k in ips.parameters:
            if k.removeprefix("_") in args:
                args[k] = args.pop(k.removeprefix("_"))

        logger.info(
            f"({self.run_id}) [STAGE]: Hook-Execute: {t_func.name}@{t_func.tag}"
        )
        rs: DictData = t_func(**param2template(args, params))

        # VALIDATE:
        #   Check the result type from hook function, it should be dict.
        if not isinstance(rs, dict):
            raise TypeError(
                f"Return type: '{t_func.name}@{t_func.tag}' does not serialize "
                f"to result model, you change return type to `dict`."
            )
        return Result(status=0, context=rs)


class TriggerStage(BaseStage):
    """Trigger Workflow execution stage that execute another workflow. This this
    the core stage that allow you to create the reusable workflow object or
    dynamic parameters workflow for common usecase.

    Data Validate:
        >>> stage = {
        ...     "name": "Trigger workflow stage execution",
        ...     "trigger": 'workflow-name-for-loader',
        ...     "params": {"run-date": "2024-08-01", "source": "src"},
        ... }
    """

    trigger: str = Field(
        description=(
            "A trigger workflow name that should already exist on the config."
        ),
    )
    params: DictData = Field(
        default_factory=dict,
        description="A parameter that want to pass to workflow execution.",
    )

    @handler_result("Raise from TriggerStage")
    def execute(self, params: DictData) -> Result:
        """Trigger another workflow execution. It will waiting the trigger
        workflow running complete before catching its result.

        :param params: A parameter data that want to use in this execution.
        :rtype: Result
        """
        # NOTE: Lazy import this workflow object.
        from . import Workflow

        # NOTE: Loading workflow object from trigger name.
        _trigger: str = param2template(self.trigger, params=params)

        # NOTE: Set running workflow ID from running stage ID to external
        #   params on Loader object.
        wf: Workflow = Workflow.from_loader(
            name=_trigger, externals={"run_id": self.run_id}
        )
        logger.info(f"({self.run_id}) [STAGE]: Trigger-Execute: {_trigger!r}")
        return wf.execute(params=param2template(self.params, params))


# NOTE:
#   An order of parsing stage model on the Job model with ``stages`` field.
#   From the current build-in stages, they do not have stage that have the same
#   fields that be cause of parsing on the Job's stages key.
#
Stage = Union[
    PyStage,
    BashStage,
    HookStage,
    TriggerStage,
    EmptyStage,
]
