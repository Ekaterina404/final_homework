import pytest

from code.downloader import get_available_formats


def test_get_available_formats():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    formats = get_available_formats(url)
    assert len(formats) > 0
    assert 'format_id' in formats[0]
    assert 'resolution' in formats[0]
    assert 'ext' in formats[0]
