from datetime import timedelta
from pydantic_settings import BaseSettings


# +---------------------------------------------------------------------------+
# |                                                                           |
# |                        Pull some settings from env                        |
# |                                                                           |
# +---------------------------------------------------------------------------+
class EnvSettings(BaseSettings):
    disable_user_create_endpoint: bool = False


env_settings = EnvSettings()


# +---------------------------------------------------------------------------+
# |                                                                           |
# |                                   Auth                                    |
# |                                                                           |
# +---------------------------------------------------------------------------+
SESSION_AGE_LIMIT = timedelta(days=1)


# +---------------------------------------------------------------------------+
# |                                                                           |
# |                        Enable / Disable Endpoints                         |
# |                                                                           |
# +---------------------------------------------------------------------------+
DISABLE_USER_CREATE_ENDPOINT = env_settings.disable_user_create_endpoint
