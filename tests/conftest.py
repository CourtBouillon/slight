from os import environ
from pathlib import Path

from pytest import fixture

for variable in ('slideshows', 'themes'):
    environ[f'SLIGHT_{variable.upper()}'] = ':'.join(
        str(group) for group in (Path(__file__).parent / variable).iterdir())

from slight import app  # noqa

test_app = fixture(lambda: app.test_client())
