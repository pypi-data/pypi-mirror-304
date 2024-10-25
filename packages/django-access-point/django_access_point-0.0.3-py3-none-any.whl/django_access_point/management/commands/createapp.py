import os
import importlib.resources
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Creates a Django app directory structure for the given app name and custom files"

    package_name = 'django_access_point'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='Name of the app to create')

    def handle(self, *args, **options):
        app_name = options['app_name']  # Get the app name from the options
        app_path = os.path.join(os.getcwd(), app_name)

        if os.path.exists(app_path):
            raise CommandError(f'App "{app_name}" already exists.')

        # Create the app directory structure
        os.makedirs(app_path)
        self.create_model_file(app_path)
        self.create_view_file(app_path)
        self.create_url_file(app_path)

        self.stdout.write(self.style.SUCCESS(f'App "{app_name}" created successfully!'))

    def create_model_file(self, app_path):
        package_name = self.package_name

        # Read the source content of 'models.py'
        try:
            models_content = importlib.resources.read_text(package_name, 'management/source_files/source_models.txt')
        except FileNotFoundError:
            raise CommandError(f'The specified source file in the package "{package_name}" could not be found.')

        # Create a 'models.py' file in the new app
        models_file_path = os.path.join(app_path, 'models.py')
        with open(models_file_path, 'w') as models_file:
            models_file.write(models_content)

    def create_view_file(self, app_path):
        package_name = self.package_name

        # Read the source content of 'models.py'
        try:
            models_content = importlib.resources.read_text(package_name, 'management/source_files/source_views.txt')
        except FileNotFoundError:
            raise CommandError(f'The specified source file in the package "{package_name}" could not be found.')

        # Create a 'models.py' file in the new app
        models_file_path = os.path.join(app_path, 'views.py')
        with open(models_file_path, 'w') as models_file:
            models_file.write(models_content)

    def create_url_file(self, app_path):
        package_name = self.package_name

        # Read the source content of 'models.py'
        try:
            models_content = importlib.resources.read_text(package_name, 'management/source_files/source_urls.txt')
        except FileNotFoundError:
            raise CommandError(f'The specified source file in the package "{package_name}" could not be found.')

        # Create a 'models.py' file in the new app
        models_file_path = os.path.join(app_path, 'urls.py')
        with open(models_file_path, 'w') as models_file:
            models_file.write(models_content)

