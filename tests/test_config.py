import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from config import validate_config, save_config, load_config, get_invalid_config_fields
import config


def test_validate_config_with_valid_values():
    config = {
        "retention_days": 30,
        "cleanup_on_startup": False
    }

    assert validate_config(config) is True


def test_validate_config_with_invalid_retention():
    config = {
        "retention_days": 90,
        "cleanup_on_startup": False
    }

    assert validate_config(config) is False


def test_validate_config_with_invalid_cleanup_type():
    config = {
        "retention_days": 30,
        "cleanup_on_startup": "False"
    }

    assert validate_config(config) is False


def test_validate_config_with_invalid_structure():
    config = ["30", False]

    assert validate_config(config) is False


def test_load_config(tmp_path, monkeypatch):
    test_file = tmp_path / "config.json"
    monkeypatch.setattr(config, "config_file", test_file)

    settings = {
        "retention_days": 15,
        "cleanup_on_startup": True
    }

    save_config(settings)
    loaded_config = load_config()

    assert loaded_config == settings


def test_load_corrupted_config(tmp_path, monkeypatch):
    test_file = tmp_path / "config.json"
    monkeypatch.setattr(config, "config_file", test_file)

    test_file.write_text("{ configuração inválida }", encoding="utf-8")

    with pytest.raises(ValueError, match="corrompido"):
        load_config()

    assert test_file.read_text(encoding="utf-8") == "{ configuração inválida }"


def test_load_missing_config(tmp_path, monkeypatch):
    test_file = tmp_path / "config.json"
    monkeypatch.setattr(config, "config_file", test_file)

    loaded_config = load_config()

    assert loaded_config is None
    assert not test_file.exists()


def test_get_invalid_config_fields():
    settings = {
        "retention_days": 90,
        "cleanup_on_startup": "False"
    }

    invalid_fields = get_invalid_config_fields(settings)

    assert invalid_fields == [
        "retention_days",
        "cleanup_on_startup"
    ]