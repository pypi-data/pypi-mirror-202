import asyncio
import inspect
import typing

from decohints import decohints
from discord.ext import commands


def is_coro(func: typing.Callable) -> bool:
    return inspect.iscoroutinefunction(func)


def is_bot(bot: object) -> bool:
    return isinstance(bot, commands.Bot)


def runner(
    property: typing.Union[typing.Callable, typing.Coroutine], *args, **kwargs
) -> typing.Optional[typing.Any]:
    return (
        property(*args, **kwargs)
        if not is_coro(property)
        else asyncio.run(property(*args, **kwargs))
    )


@decohints  # YOU SAVED ME NOW I CAN SEE FUNCTION TYPINGS
def prevent_calling_outside_dpyhr(func: typing.Callable) -> typing.Callable:
    def wrapper(
        *args,
        **kwargs,
    ) -> typing.Callable:
        # check stack if it's not called by dpyhr.run then raise warning
        if not any("__init__.py" in frame.filename for frame in inspect.stack()):
            raise RuntimeError(
                "This function is not intended to be called outside dpyhr.run. Please use dpyhr.run instead."
            )
        return func(
            *args,
            **kwargs,
        )

    return wrapper
