from chibi.config import configuration

if not configuration.gitlab.host:
    configuration.gitlab.host = 'gitlab.com'
if not configuration.github.schema:
    configuration.gitlab.schema = 'https'
