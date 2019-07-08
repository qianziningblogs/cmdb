# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']

REDIS = {
    "host": "127.0.0.1",
    "port": 6379,
    "password":""
}


CELERY_IMPORTS = (
    'servers.tasks',
    'scheduler.tasks'
)
CELERY_BROKER_URL = 'redis://:{}@{}:{}/0'.format(REDIS['password'],REDIS['host'], REDIS['port'])
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'redis://:{}@{}:{}/0'.format(REDIS['password'],REDIS['host'], REDIS['port'])
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cmdb',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '',
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    
    'formatters': {
        'verbose': {
            'format': '%(levelname)s|%(asctime)s|%(module)s|%(message)s'
            # 'format': '%(asctime)s %(levelname)s %(relativeCreated)d %(created)f %(filename)s %(levelno)s %(module)s %(funcName)s %(lineno)d %(msecs)d %(name)s %(message)s'
        },
        'simple': {
            'format': '%(asctime)s|%(levelname)s|%(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        
        'cmdb_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'cmdb_info.log',
            'maxBytes': 10240000,
            'formatter': 'verbose',
            'backupCount': 5,
        },
        
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['cmdb_info'],
            'propagate': True,
        },
        
    },
}

CMDB_DOMAIN = "cmdb.sinochem.cloud"
