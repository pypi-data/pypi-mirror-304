import os

VINZ_URL = os.getenv('VINZ_URL') or 'https://vinz.atlasai.co'

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN') or 'dev-demand-intelligence.us.auth0.com'  # e.g., 'example.auth0.com'
CLIENT_ID = os.getenv('AUTH0_CLIENT_ID') or '8YDYKZMNDbW8qwzA9wJqaIcV2nlQ8ie3'
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE') or 'dev-management-api.atlasai.co'

AUTH0_TOKEN_URL = f'https://{AUTH0_DOMAIN}/oauth/token'
AUTH0_AUTHORIZE_URL = f'https://{AUTH0_DOMAIN}/authorize'

SCOPES = 'openid profile email'

MAX_WAIT_TIME_LOGIN = 100

DEFAULT_POLLING_TIMEOUT = 3600
POLLING_INTERVAL = 10

DEFAULT_PAGE_SIZE = 20
DISABLE_SSL_VERIFICATION = 'DISABLE_SSL_VERIFICATION'
