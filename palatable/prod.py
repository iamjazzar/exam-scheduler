''' Django production settings for palatable project. '''

from .base import *

DEBUG = False

TEMPLATE_DEBUG = False

IS_LIVE = True

ALLOWED_HOSTS = [
'*'
]
