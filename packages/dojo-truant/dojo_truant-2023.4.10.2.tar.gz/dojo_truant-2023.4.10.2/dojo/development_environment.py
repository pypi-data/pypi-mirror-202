#!/usr/bin/env python3

import logging
import urllib.parse
import string

import requests

import dojo

class Development_Environment(dojo.DAPI):
    _endpoint = string.Template("/api/v2/development_enviornments/${id}/")
    _post_endpoint = "/api/v2/development_environments/"
    _search_endpoint = "/api/v2/development_environments/"

    _model_validation = {
        "name": {"type": str,
                  "required": True},
    }

    _obj_iterate = ".results[]"

    _type = "development_environment"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger("DAPI.Test")
