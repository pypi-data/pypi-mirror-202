import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin_form_image_preivew.settings")

application = get_wsgi_application()
