import os
import io
import sys
import django
from django.core.management import call_command

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'h_t_handcraft.settings')  # Replace 'your_project' with the actual name of your project

# Set up Django
django.setup()

# Redirect output to a file with utf-8 encoding
with io.open('backup_data.json', 'w', encoding='utf-8') as f:
    sys.stdout = f  # Redirect standard output to the file
    call_command('dumpdata', indent=4)
