from django.core.management.base import BaseCommand
from accounts.models import Role, User, StudentProfile


class Command(BaseCommand):
    help = 'Create a test student user'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test student...')

        # Ensure STUDENT role exists
        student_role, _ = Role.objects.get_or_create(name='STUDENT')

        # Create test student user
        username = 'teststudent'
        email = 'student@test.com'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))
            return

        user = User.objects.create_user(
            username=username,
            email=email,
            password='password123',
            first_name='Test',
            last_name='Student',
            role=student_role,
            is_active=True
        )

        # Create student profile
        StudentProfile.objects.create(
            user=user,
            student_id='ST2024001',
            department='Computer Science',
            year=2,
            gender='MALE'
        )

        self.stdout.write(self.style.SUCCESS(
            f'\nTest student created successfully!'
            f'\nUsername: {username}'
            f'\nPassword: password123'
            f'\nEmail: {email}'
        ))
