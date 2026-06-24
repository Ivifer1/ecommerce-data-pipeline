"""
Tests para transform.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from scripts.transform import transform_categories, transform_products


def test_transform_categories():
    """Test: extrae categorias unicas."""
    raw = [
        {"id": 1, "category": "electronics"},
        {"id": 2, "category": "jewelery"},
        {"id": 3, "category": "electronics"},
    ]
    
    result = transform_categories(raw)
    
    assert len(result) == 2
    assert list(result["name"]) == ["electronics", "jewelery"]


def test_transform_products():
    """Test: transforma productos con categoria mapeada."""
    raw = [{
        "id": 1,
        "title": "Test Product",
        "price": 10.99,
        "description": "A test",
        "category": "electronics",
        "image": "http://test.jpg",
        "rating": {"rate": 4.5, "count": 100}
    }]
    
    categories = pd.DataFrame({"id": [1], "name": ["electronics"]})
    result = transform_products(raw, categories)
    
    assert len(result) == 1
    assert result.iloc[0]["title"] == "Test Product"
    assert result.iloc[0]["price"] == 10.99
    assert result.iloc[0]["category_id"] == 1