from src.ai_generation.bpmn_agent.nodes._extract_system_and_configuration import (
    extract_system_and_config,
)


def test_extracts_system_prompt_and_returns_rest():
    config = {"system_prompt": "You are a BPMN analyst", "temperature": 0.7}

    system, config_copy = extract_system_and_config(config)

    assert system == "You are a BPMN analyst"
    assert config_copy == {"temperature": 0.7}


def test_returns_none_when_no_system_prompt():
    config = {"temperature": 0.5}

    system, config_copy = extract_system_and_config(config)

    assert system is None
    assert config_copy == {"temperature": 0.5}


def test_does_not_mutate_original_dict():
    config = {"system_prompt": "hello", "temperature": 0.3}

    extract_system_and_config(config)

    assert config == {"system_prompt": "hello", "temperature": 0.3}


def test_returns_copy_not_same_object():
    config = {"temperature": 0.5}

    _, config_copy = extract_system_and_config(config)

    assert config_copy is not config
