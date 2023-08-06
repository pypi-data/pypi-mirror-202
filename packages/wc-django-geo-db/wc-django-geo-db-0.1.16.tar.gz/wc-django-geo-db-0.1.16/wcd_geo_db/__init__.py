__version__ = '0.1.16'

from .const import *

VERSION = tuple(__version__.split('.'))

default_app_config = 'wcd_geo_db.apps.GeoDBConfig'
