"""NtcPlot is a cross-platform netcdf plotting package.

More information is available at http://pypi.python.org/pypi/ntcplot
"""

import sys
from .values import version


#: The release version
__version__ = version

MIN_PYTHON_VERSION = 3, 12
MIN_PYTHON_VERSION_STR = ".".join([str(v) for v in MIN_PYTHON_VERSION])

if sys.version_info < MIN_PYTHON_VERSION:
    msg = f"NtcPlot {version} requires Python {MIN_PYTHON_VERSION_STR} or newer."
    raise Exception(msg)


