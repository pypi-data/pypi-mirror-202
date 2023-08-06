"""
dphyr
A simple module for support hot reloading of discord.py "cogs" (extensions).
"""
import enum
import typing

from .log_dummy import Logger

log = Logger("dpyhr")
log.setLevel(0)

enable_log_bool = False

try:
    import discord.ext.commands as commands
except ImportError as e:
    log.critical(
        "dpyhr detected that discord.py is not found or you're using wrong version of discord.py without discord.ext.commands. Please install one. For reasons why I am not shipped with discord.py please read this.\nhttps://github.com/timelessnesses/dpyhr/blob/main/README.md#why-you-dont-shipped-discordpy-with-this-package"
    )
    raise ImportError(
        "dpyhr detected that discord.py is not found or you're using wrong version of discord.py without discord.ext.commands. Please install one. For reasons why I am not shipped with discord.py please read this.\nhttps://github.com/timelessnesses/dpyhr/blob/main/README.md#why-you-dont-shipped-discordpy-with-this-package"
    )

from . import normal, polling
from .utils import is_bot


class Selection(enum.Enum):

    polling: polling = polling
    normal: normal = normal


def run(
    *paths: str,
    bot: commands.Bot = None,
    selection: Selection = Selection.normal,
    reloader: typing.Callable = None,
    conditional: typing.Callable = None,
    recursive: bool = False,
    **kwargs,
) -> None:
    """Run dphyr in another thread.

    Args:
        *paths (str): Paths you want to watch for cogs. Supply those as argument
        bot (commands.Bot, Optional): For reloading extensions (if reloader doesn't exists)
        selection (Selection, optional): Observer selection. Defaults to Selection.normal.
        reloader (typing.Callable, optional): Reload module with your own function. Defaults to None.
        conditional (typing.Callable, optional): Conditional when event is triggered. Defaults to None.
        recursive (bool, optional): Recursive reloading. Defaults to False.
        **kwargs: Other arguments for observer.
    Returns:
        None: No returns.
    """
    if (not bot or not is_bot(bot)) and not reloader:
        log.critical("No reloader found and can't fallback to bot.reload_extension")
        raise ValueError("No reloader found")
    if not reloader:
        log.warn("No custom reloader found. Falling back to bot.reload_extension")
        reloader = bot.reload_extension
    if not conditional:
        log.warn(
            "No custom conditional function found. Falling back to lambda function that detects if file changed it .py file"
        )
        conditional = lambda event: event.src_path.endswith(".py")

    try:
        Selection(selection)
    except:
        log.critical("Invalid selection")
        raise ValueError("Invalid selection")
    if enable_log_bool:
        selection.value.enable_log()
    else:
        selection.value.disable_log()
    selection.value.start(
        *paths,
        reloader=reloader,
        condition=conditional,
        recursive=recursive,
        **kwargs,
    )
    log.info(f"Started {selection.value} observer in another thread")


def enable_log():
    import logging

    global log, enable_log_bool
    log = logging.getLogger("dpyhr")
    enable_log_bool = True


def disable_log():
    global log, enable_log_bool
    log = Logger("dpyhr")
    enable_log_bool = False


log.info("fully initalized")
