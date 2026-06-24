"""
Tests para extract.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.extract import fetch_data, save_raw_data
from unittest.mock import Mock, patch


def test_fetch_data_success():
    """Test: fetch_data devuelve datos cuando la API responde 200."""
    with patch("scripts.extract.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = [{"id": 1, "title": "Test"}]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = fetch_data("/products")

        assert result == [{"id": 1, "title": "Test"}]


def test_fetch_data_failure():
    """Test: fetch_data lanza error cuando la API falla."""
    with patch("scripts.extract.requests.get") as mock_get:
        from requests import HTTPError
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("404")
        mock_get.return_value = mock_response

        try:
            fetch_data("/products")
            assert False, "Deberia haber lanzado HTTPError"
        except HTTPError:
            pass


def test_save_raw_data(tmp_path):
    """Test: save_raw_data crea un archivo JSON."""
    import json
    from scripts.extract import save_raw_data
    
    with patch("scripts.extract.DATA_RAW_DIR", tmp_path):
        data = [{"id": 1, "name": "test"}]
        result = save_raw_data(data, "test.json")
        
        assert result.exists()
        with open(result, "r") as f:
            content = json.load(f)
        assert content == data