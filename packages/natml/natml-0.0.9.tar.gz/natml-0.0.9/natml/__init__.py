# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from os import environ

api_url = "https://staging.api.natml.ai/graph" if environ.get("NATML_STAGING", None) else "https://api.natml.ai/graph"
access_key: str = None

from .api import *
from .version import __version__