from contextlib import contextmanager
from multiprocessing import Process
from os.path import realpath
from pathlib import Path
from re import compile as regex
from subprocess import check_output
from time import sleep
from typing import Callable, Any, Tuple, Optional

from pytest import mark
from typeguard import typechecked


VAGRANT_RUNNING_PAT = regex(r'rabbitmq-vm\s+running \(libvirt\)')
VAGRANT_CWD = Path(realpath(__file__)).parent.parent.parent


@contextmanager
def sub_process(target: Callable, args: Optional[Tuple[Any, ...]] = None,
                name: Optional[str] = None,
                terminate: bool = True):
    proc = Process(target=target, args=args or (), name=name)
    proc.start()
    try:
        sleep(0.2)
        yield proc
    finally:
        if terminate:
            proc.terminate()
        proc.join()


@typechecked
def vagrant_up() -> bool:
    return bool(VAGRANT_RUNNING_PAT.search(
        check_output(['vagrant', 'status', 'rabbitmq-vm'], cwd=VAGRANT_CWD).decode()))


vagrant_test = mark.skipif(not vagrant_up(), reason="rabbitmq-vm needs to be running")