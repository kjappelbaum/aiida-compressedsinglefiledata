# -*- coding: utf-8 -*-
"""
For pytest
initialise a test database and profile
"""
from __future__ import absolute_import
import tempfile
import shutil
import os
import pytest

from aiida.manage.fixtures import fixture_manager


def get_backend_str():
    """ Return database backend string.
    Reads from 'TEST_AIIDA_BACKEND' environment variable.
    Defaults to django backend.
    """
    from aiida.backends.profile import BACKEND_DJANGO, BACKEND_SQLA
    backend_env = os.environ.get('TEST_AIIDA_BACKEND', BACKEND_DJANGO)
    if backend_env in (BACKEND_DJANGO, BACKEND_SQLA):
        return backend_env

    raise ValueError("Unknown backend '{}' read from TEST_AIIDA_BACKEND environment variable".format(backend_env))


@pytest.fixture(scope='session')
def aiida_profile():
    """setup a test profile for the duration of the tests"""
    with fixture_manager() as fixture_mgr:
        yield fixture_mgr


@pytest.fixture(scope='module')
def imp(aiida_profile):  # pylint:disable=unused-argument, redefined-outer-name
    """do some imports"""
    from aiida.orm import load_node

    return load_node


@pytest.fixture(scope='function')
def clear_database(aiida_profile):  # pylint:disable=unused-argument, redefined-outer-name
    """clear the database after each test"""
    yield
    aiida_profile.reset_db()


@pytest.fixture(scope='function')
def new_workdir():
    """get a new temporary folder to use as the computer's workdir"""
    dirpath = tempfile.mkdtemp()
    yield dirpath
    shutil.rmtree(dirpath)
