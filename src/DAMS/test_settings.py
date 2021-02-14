from .settings import *             # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'DAMS',
        # 'CLIENT': {
        #    'host': 'your-db-host',
        # }
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
