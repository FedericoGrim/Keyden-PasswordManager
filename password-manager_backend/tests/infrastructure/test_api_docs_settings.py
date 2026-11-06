import pytest

from infrastructure.settings import api_docs_enabled


@pytest.mark.parametrize("value", [None, "", "false", "0", "no"])
def test_docs_are_disabled_by_default(value: str | None) -> None:
    assert api_docs_enabled(value) is False


@pytest.mark.parametrize("value", ["true", "TRUE", "1", "yes", " true "])
def test_docs_are_enabled_in_debug(value: str) -> None:
    assert api_docs_enabled(value) is True
