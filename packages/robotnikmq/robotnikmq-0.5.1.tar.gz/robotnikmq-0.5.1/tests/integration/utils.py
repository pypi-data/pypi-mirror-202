from contextlib import contextmanager
from multiprocessing import Process
from subprocess import run
from time import sleep
from typing import Callable, Any, Tuple, Optional

from pytest_rabbitmq import factories

# pylint: disable=E0401
from pytest_rabbitmq.factories.executor import RabbitMqExecutor  # type: ignore

# pylint: enable=E0401
from pytest import fixture

from robotnikmq.config import server_config, RobotnikConfig, conn_config

USERNAME = "robotnik"
PASSWORD = "hackme"
VIRTUAL_HOST = "/robotnik"

META_QUEUE = "skynet.legion"


@contextmanager
def sub_process(
    target: Callable,
    args: Optional[Tuple[Any, ...]] = None,
    name: Optional[str] = None,
    terminate: bool = True,
):
    proc = Process(target=target, args=args or (), name=name)
    proc.start()
    try:
        sleep(0.2)
        yield proc
    finally:
        if terminate:
            proc.terminate()
        proc.join()


def initialize_rabbitmq(proc: RabbitMqExecutor):
    run(
        [
            proc.rabbit_ctl,
            "--quiet",
            "-n",
            f"rabbitmq-test-{proc.port}",
            "add_user",
            USERNAME,
            PASSWORD,
        ],
        check=False,
    )
    run(
        [
            proc.rabbit_ctl,
            "--quiet",
            "-n",
            f"rabbitmq-test-{proc.port}",
            "add_vhost",
            VIRTUAL_HOST,
            "--description",
            "Used for testing RobotnikMQ",
        ],
        check=False,
    )
    run(
        [
            proc.rabbit_ctl,
            "--quiet",
            "-n",
            f"rabbitmq-test-{proc.port}",
            "set_permissions",
            "-p",
            VIRTUAL_HOST,
            USERNAME,
            ".*",
            ".*",
            ".*",
        ],
        check=False,
    )


def config_for(
    proc: RabbitMqExecutor, attempts: int = 1, min_wait: int = 1, max_wait: int = 2
) -> RobotnikConfig:
    return RobotnikConfig(
        connection=conn_config(attempts, min_wait, max_wait),
        tiers=[[server_config(proc.host, proc.port, USERNAME, PASSWORD, VIRTUAL_HOST)]],
    )


@fixture(scope="module")
def robotnikmq_config(rabbitmq_proc):
    initialize_rabbitmq(rabbitmq_proc)
    return config_for(rabbitmq_proc)


@fixture(scope="module")
def robotnikmq():
    robotnikmq_proc = factories.rabbitmq_proc(port=8888)
    initialize_rabbitmq(robotnikmq_proc)
    return robotnikmq_proc
