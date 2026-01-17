from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Role

class Command(BaseCommand):
    help = 'Creates initial roles and super admin user'

    def handle(self, *args, **kwargs):
        # Create Roles
        roles = ['ADMIN', 'WARDEN', 'STUDENT']
        for role_name in roles:
            Role.objects.get_or_create(name=role_name)
        self.stdout.write(self.style.SUCCESS('Roles created/verified'))

        # Create Admin User
        User = get_user_model()
        admin_email = 'hanan@gmail.com'
        admin_pass = '987654321'
        
        if not User.objects.filter(username=admin_email).exists():
            admin_role = Role.objects.get(name='ADMIN')
            user = User.objects.create_superuser(
                username=admin_email,
                email=admin_email,
                password=admin_pass,
                role=admin_role
            )
            self.stdout.write(self.style.SUCCESS(f'Super admin created: {admin_email}'))
        else:
            self.stdout.write(self.style.WARNING(f'User {admin_email} already exists'))
