import pytest
from pathlib import Path
import logging

from src.ai_generation.managers.llm_config import LLMConfigManager


# --- FIXTURES ---
@pytest.fixture
def config_dir(tmp_path) -> Path:
    dir = tmp_path / "prompts"
    dir.mkdir()
    return dir


@pytest.fixture
def manager(config_dir):
    # Clear cache after testing
    LLMConfigManager._load_file.cache_clear()
    return LLMConfigManager(config_dir=str(config_dir))


# --- TESTS ---
def test_get_config_happy_path(config_dir, manager):
    """
    Test that load_file loads configs correctly.
    Variables should be parsed by Jinja2
    """
    # Add test config file
    config = """
    temperature: 0.7
    system_prompt: |
        Test promt by a {{ role }}
    """
    (config_dir / "test.yaml").write_text(config, encoding="UTF-8")

    # Call with test config file
    result = manager.get_call_config("test", role="Test")

    # Verify config is parsed
    assert result == {
        "temperature": 0.7,
        "system_prompt": "Test promt by a Test\n",
    }  # Check test config


def test_get_config_load_fail(config_dir, manager, caplog):
    """
    Test that load_file fails gracefully when file not found.
    Also catches logger message
    """

    with caplog.at_level(level=logging.INFO):
        result = manager.get_call_config("nonexistent")

    assert result == {}  # Should be empty if Error occurred
    assert "Failed to load file at" in caplog.text  # Verify message


def test_bad_yaml(manager, config_dir, caplog):
    """
    Test: what if yaml structure broken
    Should return {} and error with YAML parsing
    """
    broken = "\tname:\n {{ username }}\n\t"

    (config_dir / "test.yaml").write_text(broken, encoding="utf-8")

    with caplog.at_level(level=logging.INFO):
        result = manager.get_call_config("test")

    assert "Failed to load YAML:" in caplog.text
    assert result == {}  # Should be empty if Error occurred


def test_jinja_rendering_failure(manager, config_dir):
    """
    Test: what if some render argument missing
    Jinja2 leaves (Undefined) by default,
    but this must do not break YAML, if stucture correct.
    """
    (config_dir / "missing_var.yaml").write_text(
        "name: {{ username }}", encoding="utf-8"
    )

    # Do not set username
    result = manager.get_call_config("missing_var")
    assert result["name"] is None or result["name"] == ""
