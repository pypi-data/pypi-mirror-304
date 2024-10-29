Use ``clock_nanosleep()`` with ``CLOCK_MONOTONIC`` to sleep. So that the sleep is not affected by system date/time jumps.

Only provide source code distribution, user need to install the build toolchain. It can't be compiled on platforms without ``clock_nanosleep()``.

On CPython 3.11+, `time.sleep() <https://docs.python.org/3/library/time.html#time.sleep>`_ function already use this method.

.. sourcecode:: python

    try:
        from clock_nanosleep import sleep
    except ImportError:
        from time import sleep

    sleep(secs)
