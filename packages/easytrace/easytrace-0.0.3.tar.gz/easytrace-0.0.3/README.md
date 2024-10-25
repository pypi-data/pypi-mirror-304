# easytrace

A lightweight tracing library for python3, it provides an alternative to attaching a heavy debugger and manually printing out arguments when you enter functions.

### Installation

Install from the [PyPi project](https://pypi.org/project/easytrace/) using pip:

```
pip install easytrace
```

There are no dependencies required other than Python3!

### Usage 

#### Basic

First import the `trace` decorator at the top of your file, setting the logging level as desired. Note, easytrace uses the `DEBUG` log level by default. Although this can be changed.
A full example can be found in `tests/test.py`

```
from easytrace.trace import trace

import logging
logging.basicConfig(level=logging.DEBUG)
```

Simply add the `@trace` decorator above and function/method you would like to trace.

```
@trace
def add_integers(a: int, b: int) -> int:
    return a + b
```

Invoking this with `add_integers(2, 3)` will produce the following trace:

```
DEBUG:easytrace:call     add_integers(a : str = 2, b : str = 3)
DEBUG:easytrace:return   add_integers -> int = 5
```

#### Parameters

The decorator has the following parameters:

```
enter - Custom string to display when entering function, overrides default
exit  - Custom string to display when leaving function, overrides default
arg_value - Should display argument values in trace
return_value - Should display return value in trace
log_level - Log level to use for this trace, overrides default
stream - Additional stream to write to for this trace, overrides default
```

An example of not logging the return value at the INFO logging level is as follows:

```
@trace(return_value=False, log_level=logging.INFO)
def function(s: str) -> str:
    ...
```

#### Default Options

To set default options, do the following:

```
from easytrace.trace import TraceConfig

TraceConfig.set_stream(open("log.log", "w")) # will set the default logging stream (excluding stdout) to the file "log.log"
TraceConfig.set_logging_level(logging.INFO)  # will set the default logging level to INFO
```