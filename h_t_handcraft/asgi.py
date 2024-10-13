import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'h_t_handcraft.settings')

application = get_asgi_application()
