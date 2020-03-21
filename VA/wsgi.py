import os

from django.core.wsgi import get_wsgi_application

# setting up SECRET_KEY
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/VA-boutique')
load_dotenv(os.path.join(project_folder, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VA.settings')

application = get_wsgi_application()
