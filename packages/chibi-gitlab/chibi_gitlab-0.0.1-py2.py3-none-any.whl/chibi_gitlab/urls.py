# -*- coding: utf-8 -*-
from chibi_gitlab.config import configuration
from chibi_requests import Chibi_url
from chibi_requests.auth import Token


base_url = Chibi_url(
    f"{configuration.gitlab.schema}://{configuration.gitlab.host}/api/v4" )

base_url += Token( name='Bearer', token=configuration.gitlab.personal_token )

projects = base_url + 'projects'
merge_requests = base_url + 'merge_requests'
