try:
    from asyncio import to_thread  # pylint: disable=unused-import
except ImportError:
    from asyncio import get_running_loop
    from contextvars import copy_context
    from functools import partial

    # Taken from the Python 3.9 source code, with slight modification.
    async def to_thread(func, *args, **kwargs):
        """
        Asynchronously run function *func* in a separate thread.

        Any *args and **kwargs supplied for this function are directly passed
        to *func*. Also, the current :class:`contextvars.Context` is propogated,
        allowing context variables from the main thread to be accessed in the
        separate thread.

        Return a coroutine that can be awaited to get the eventual result of *func*.
        """
        loop = get_running_loop()
        ctx = copy_context()
        func_call = partial(ctx.run, func, *args, **kwargs)
        return await loop.run_in_executor(None, func_call)
