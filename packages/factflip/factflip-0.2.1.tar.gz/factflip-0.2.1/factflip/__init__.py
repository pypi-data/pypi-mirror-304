import os

from platformdirs import user_data_path
from usingversion import getattr_with_version

APPNAME = "factflip"
APP_REPOSITORY = "https://github.com/evhart/factflip"
DEFAULT_ROOT_PATH = user_data_path(appname=APPNAME)
DEFAULT_EMBEDDINGS_PATH = os.path.join(DEFAULT_ROOT_PATH, "factflip_embeddings")
DEFAULT_TEMPLATES_PATH = os.path.join(DEFAULT_ROOT_PATH, "templates")

__getattr__ = getattr_with_version(APPNAME, __file__, __name__)
