LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console_debug': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'debug_console',
            'filters': ['debug_only']
        },
        'console_warning': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'warning_console_error_email',
            'filters': ['debug_only']
        },
        'console_error': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'error_console_file',
            'filters': ['debug_only']
        },

        'general_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'general_log_file',
            'filename': 'logs/general.log',
            'filters': ['not_debug']
        },
        'errors_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'error_console_file',
            'filename': 'logs/errors.log',
            'filters': ['not_debug']
        },
        'security_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'security_file',
            'filename': 'logs/security.log',
            'filters': ['not_debug']
        },
        'mail_to_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'warning_console_error_email',
            'filters': ['not_debug']
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console_debug', 'console_warning', 'console_error', 'general_file'],
            'level': 'DEBUG'
        },
        'django.request': {
            'handlers': ['errors_file', 'mail_to_admins'],
            'level': 'DEBUG'
        },
        'django.server': {
            'handlers': ['errors_file', 'mail_to_admins'],
            'level': 'DEBUG'
        },
        'django.template': {
            'handlers': ['errors_file'],
            'level': 'DEBUG'
        },
        'django.db.backends': {
            'handlers': ['errors_file'],
            'level': 'DEBUG'
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'DEBUG'
        },
    },
    'formatters': {
        'debug_console': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
        'warning_console_error_email': {
            'format': '%(asctime)s - %(levelname)s - %(message)s - %(pathname)s'
        },
        'error_console_file': {
            'format': '%(asctime)s - %(levelname)s - %(message)s - %(pathname)s - %(exc_info)s'
        },
        'general_log_file': {
            'format': '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
        },
        'security_file': {
            'format': '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
        },
    },
    'filters': {
        'debug_only': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
        'not_debug': {
            '()': 'django.utils.log.RequireDebugFalse'
        },

    },
}
