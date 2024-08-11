from . import version
from brothers.data import Data
from brothers.windows import MainWindow

__version__ = version.version
__author__ = "Poivron Jaune"
__author_email__ = "poivronjaune@gmail.com"
__short_description__ = "Trading simulator for multi-asset analysis"

import warnings
warnings.filterwarnings('default', category=DeprecationWarning, module='^yfinance')

__all__ = ['download', 'Ticker', 'Tickers', 'enable_debug_mode', 'set_tz_cache_location']
