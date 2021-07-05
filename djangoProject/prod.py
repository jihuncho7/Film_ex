from .settings import *

STATICFILES_STORAGE = "djangoProject.storages.StaticAzureStorage"
DEFAULT_FILE_STORAGE = "djangoProject.storages.MediaAzureStorage"

# AZURE_ACCOUNT_NAME = os.environ["AZURE_ACCOUNT_NAME"]
# AZURE_ACCOUNT_KEY = os.environ["AZURE_ACCOUNT_KEY"]
AZURE_ACCOUNT_NAME = "jjhfilm"
AZURE_ACCOUNT_KEY = "Ojb0k7E9USr2LHe6ZFIV6Wm9S/w+HzNrfily5c2j7MQtDcNa/dSoCi2VmpmtSwcBw3qIvU0RcrkuYxzTsFT6aQ=="

DEBUG = os.environ.get("DEBUG") in ["1","t","true","T","True"]
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS","").split(",")
DATABASES = {
    # "default":{
    #     "ENGINE": "django.db.backends.postgresql",
    #     "HOST": os.environ["DB_HOST"],
    #     "USER": os.environ["DB_USER"],
    #     "PASSWORD": os.environ["DB_PASSWORD"],
    #     "NAME": os.environ["DB_NAME"],
    # },
    "default":{
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "filmserver.postgres.database.azure.com",
        "USER": "jjh@filmserver",
        "PASSWORD": "Qazw1739@@",
        "NAME": "postgres",
    },
}
# LOGGING = {
#     "version":1,
#     "disable_existing_loggers": False,
#     "handlers":{
#         "console":{
#     "level": "ERROR",
#     "class":"logging.StreamHandler"
# ,},
#     },
# "loggers":{
#     "django":{
#         "handlers": ["console"],
#         "level": "ERROR",
#     },
# },
# }