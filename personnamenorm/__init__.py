

__description__ = "unifying different notations of person names"
__author__ = "Klaus Lippert"
__copyright__ = "2021 by Klaus Lippert"
__license__ = "MIT"
__email__ = "klaus.lippert@mailbox.org"
__version__ = "0.2.12"

from .namenorm import *
from .downloader import *

# download of p values from github if file does not exist 
_=downloader()

