import pytest

from app.utils.validators import normalize_ticker


def test_invalid_ticker_rejected() -> None:
    with pytest.raises(ValueError):
        normalize_ticker("$bad")
