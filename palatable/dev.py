''' Django development settings for palatable project. '''

from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static', 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
