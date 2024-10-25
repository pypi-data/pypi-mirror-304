# easytrace

A very lightweight tracing library for python3, it provides an alternative to attaching a heavy debugger and manually printing out arguments when you enter functions.

### Installation

Install from the [PyPi project](https://pypi.org/project/easytrace/) using pip:

```
pip install easytrace
```

There are no dependencies required other than Python3!

### Usage 

First import the `trace` decorator at the top of your file, setting the logging level as desired. Note, easytrace uses the `DEBUG` log level by default. Although this can be changed.

```
from easytrace.trace import trace

import logging
logging.basicConfig(level=logging.DEBUG)
```

With any function or class method, simp

