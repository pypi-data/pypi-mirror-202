import traceback
import typing

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from .log_dummy import Logger
from .utils import prevent_calling_outside_dpyhr, runner

log = Logger("dpyhr.normal")


class Normal(FileSystemEventHandler):
    def __init__(self, reloader: typing.Callable, condition: typing.Callable) -> None:
        self.reload = reloader
        self.condition = condition

    def on_modified(self, event: FileSystemEvent) -> typing.NoReturn:
        log.info(f"File changed: {event.src_path}")
        if runner(self.condition, event):
            log.info("Reloading...")
            path = event.src_path.replace("\\", "/").replace("/", ".")[
                :-3
            ]  # Convert to module path :D
            try:
                runner(self.reload, path)
                log.info(f"Reloaded {path}")
            except Exception as e:
                log.error(f"Failed to reload {path}")
                log.error(e)
                log.error(traceback.format_exc())


@prevent_calling_outside_dpyhr
def enable_log():
    global log
    import logging

    log = logging.getLogger("dpyhr.normal")


@prevent_calling_outside_dpyhr
def disable_log():
    global log
    log = Logger("dpyhr.normal")


@prevent_calling_outside_dpyhr
def start(
    *paths: str,
    reloader: typing.Callable,
    condition: typing.Callable,
    recursive: bool,
    **kwargs,
) -> typing.NoReturn:
    """
    Internal function for starting normal observer.
    Please use dphyr.run() instead.
    """
    normal_observer = Observer(**kwargs)
    for path in paths:
        log.debug(f"Adding {path} to observer")
        normal_observer.schedule(Normal(reloader, condition), path, recursive=recursive)
    normal_observer.start()
    log.info("Started normal observer")
