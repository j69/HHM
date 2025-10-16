from django.core.management.base import BaseCommand, CommandError
from api.models import Organization, User

class Command(BaseCommand):
    help = 'Create an organization and a user (or attach user to existing org).'

    def add_arguments(self, parser):
        parser.add_argument('--org', required=True, help='Organization name')
        parser.add_argument('--username', required=True, help='Username')
        parser.add_argument('--email', required=False, help='Email address')
        parser.add_argument('--password', required=False, help='Password (if not set, user will be inactive)')
        parser.add_argument('--staff', action='store_true', help='Make user staff')

    def handle(self, *args, **options):
        org_name = options['org']
        username = options['username']
        email = options.get('email') or ''
        password = options.get('password')
        is_staff = options.get('staff', False)

        org, created = Organization.objects.get_or_create(name=org_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created organization {org_name} (id={org.id})'))
        else:
            self.stdout.write(self.style.WARNING(f'Using existing organization {org_name} (id={org.id})'))

        if User.objects.filter(username=username).exists():
            raise CommandError(f'User {username} already exists.')

        user = User(username=username, email=email, organization=org, is_staff=is_staff)
        if password:
            user.set_password(password)
            user.is_active = True
        else:
            user.is_active = False
        user.save()
        self.stdout.write(self.style.SUCCESS(f'Created user {username} (id={user.id}) in org {org_name}. Active: {user.is_active}'))
        if not password:
            self.stdout.write(self.style.WARNING('No password provided; user created inactive. Use the admin to set a password or provide --password.'))
