import os

from platformdirs import user_data_path

APPNAME = "factflip"
DEFAULT_ROOT_PATH = user_data_path(appname=APPNAME)
DEFAULT_EMBEDDINGS_PATH = os.path.join(DEFAULT_ROOT_PATH, "factflip_embeddings")
DEFAULT_TEMPLATES_PATH = os.path.join(DEFAULT_ROOT_PATH, "templates")
