# pylint: skip-file
import json

import pytest
from unittest.mock import MagicMock, Mock, patch


@pytest.fixture
def dummy_data():
    with open("data/astronomy_test_data.py") as f:
        return json.load(f, encoding="utf8")

def test_check_data_in_tables():
    pass