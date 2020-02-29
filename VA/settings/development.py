from VA.settings.common import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&gfm96b4n&a8i@7io^zheq)kzjd3k@vd(#(mp-*vw_kg_fr_hy'

INSTALLED_APPS += 'debug_toolbar',