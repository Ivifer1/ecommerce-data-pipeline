"""
Tests para load.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from unittest.mock import Mock, patch
from scripts.load import load_csv_to_table


def test_load_csv_to_table():
    """Test: load_csv_to_table lee CSV y llama to_sql correctamente."""
    with patch("scripts.load.pd.read_csv") as mock_read:
        # DataFrame real, pero con to_sql mockeado (monkey-patch)
        real_df = pd.DataFrame({"col1": [1, 2, 3]})
        real_df.to_sql = Mock()  # Esto evita que pandas use el engine real
        mock_read.return_value = real_df
        mock_engine = Mock()

        load_csv_to_table("test.csv", "test_table", mock_engine)

        # Verificar que se leyó el CSV
        mock_read.assert_called_once()

        # Verificar que to_sql fue llamado con los argumentos correctos
        real_df.to_sql.assert_called_once_with(
            name="test_table",
            con=mock_engine,
            if_exists="append",
            index=False
        )