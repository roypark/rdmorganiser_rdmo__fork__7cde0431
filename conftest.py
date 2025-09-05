import json
import shutil
from pathlib import Path

import pytest
from django.conf import settings
from django.core.management import call_command

from rdmo.accounts.utils import set_group_permissions


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """Fixture to set up the database with fixtures and permissions."""
    with django_db_blocker.unblock():
        fixtures = []
        for fixture_dir in settings.FIXTURE_DIRS:
            for file in Path(fixture_dir).iterdir():
                if file.stem in [
                    'accounts',
                    'conditions',
                    'domain',
                    'groups',
                    'options',
                    'overlays',
                    'projects',
                    'questions',
                    'sites',
                    'tasks',
                    'users',
                    'views'
                ]:
                    fixtures.append(file)

        call_command('loaddata', *fixtures)
        set_group_permissions()


@pytest.fixture
def files():
    """Fixture to create a temporary MEDIA_ROOT directory and copy test data into it."""
    media_path = Path(__file__).parent / 'testing' / 'media'
    media_root = Path(settings.MEDIA_ROOT)

    if media_root.exists():
        shutil.rmtree(media_root)
    shutil.copytree(media_path, media_root)


@pytest.fixture
def json_data():
    """Fixture to load json data from a file."""
    json_file = Path(settings.BASE_DIR) / 'import' / 'catalogs.json'
    json_data = {
        'elements': json.loads(json_file.read_text())
    }
    return json_data
