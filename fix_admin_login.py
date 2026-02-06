import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User

# Reset 'admin' to 'admin123' since user is trying that
try:
    admin = User.objects.get(username='admin')
    admin.set_password('admin123')
    admin.save()
    print(f"SUCCESS: Reset 'admin' password to 'admin123'")
except User.DoesNotExist:
    print("WARNING: 'admin' user not found")

# Also ensure 'hanan989' is definitely '12345678'
try:
    hanan = User.objects.get(username='hanan989')
    hanan.set_password('12345678')
    hanan.save()
    print(f"SUCCESS: Reset 'hanan989' password to '12345678'")
except User.DoesNotExist:
    print("WARNING: 'hanan989' user not found")
