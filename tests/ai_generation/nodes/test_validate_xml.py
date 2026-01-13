import logging
import pytest
from lxml import etree

from src.ai_generation.bpmn_agent.simple.nodes.validate_xml import (
    _clean_xml,
    validate_xml,
)
from src.ai_generation.bpmn_agent.simple.state import SimpleBPMNAgent


@pytest.fixture
def test_state():
    yield {
        "user_prompt": "",
        "user_edit_promt": "",
        "thread_id": "",
        "xml_content": "TESTING XML THERE",
        "clean_xml": "",
        "is_valid": False,
        "validation_error": None,
        "previous_answer": "",
    }


class TestCleanXml:
    """Tests for the _clean_xml function"""

    def test_clean_xml_with_markdown_tags(self):
        """Test cleaning XML wrapped in ```xml ``` markdown tags"""
        raw_xml = """```xml
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL">
    <bpmn:process id="Process_1" />
</bpmn:definitions>
```"""
        result = _clean_xml(raw_xml)
        assert result.startswith("<bpmn:definitions")
        assert "```xml" not in result
        assert "```" not in result

    def test_clean_xml_without_markdown_tags(self):
        """Test cleaning XML without markdown tags returns the same content"""
        raw_xml = """<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL">
    <bpmn:process id="Process_1" />
</bpmn:definitions>"""
        result = _clean_xml(raw_xml)
        assert result == raw_xml

    def test_clean_xml_with_backticks_at_start(self):
        """Test cleaning XML with triple backticks at the beginning"""
        raw_xml = """```<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL">
    <bpmn:process id="Process_1" />
</bpmn:definitions>```
"""
        result = _clean_xml(raw_xml)
        assert result.startswith("<bpmn:definitions")
        assert "```" not in result

    def test_clean_xml_strips_whitespace(self):
        """Test that _clean_xml strips leading and trailing whitespace"""
        raw_xml = """   
```xml
<bpmn:process id="test" />
```
   
"""
        result = _clean_xml(raw_xml)
        assert result.strip() == '<bpmn:process id="test" />'


class TestValidateXml:
    """Tests for the validate_xml function"""

    def test_validate_xml_valid_bpmn(self, test_state):
        """Test validation of a valid BPMN XML"""
        valid_xml = """<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <bpmn:process id="Process_1" isExecutable="false">
        <bpmn:startEvent id="StartEvent_1" />
    </bpmn:process>
</bpmn:definitions>"""
        test_state["xml_content"] = valid_xml

        result = validate_xml(test_state)

        assert result["is_valid"] is True
        assert result["clean_xml"] is not None
        assert result["validation_error"] is None
        assert "<bpmn:definitions" in result["clean_xml"]

    def test_validate_xml_invalid_syntax(self, test_state):
        """Test validation fails for invalid XML syntax"""
        invalid_xml = "<bpmn:process id='test' ><invalid_tag>"
        test_state["xml_content"] = invalid_xml

        result = validate_xml(test_state)

        assert result["is_valid"] is False
        assert result["clean_xml"] is None
        assert result["validation_error"] is not None
        assert "XML Syntax Error" in result["validation_error"]

    def test_validate_xml_unclosed_tag(self, test_state):
        """Test validation fails for unclosed tag"""
        invalid_xml = "<bpmn:process><bpmn:startEvent></bpmn:process>"
        test_state["xml_content"] = invalid_xml

        result = validate_xml(test_state)

        assert result["is_valid"] is False
        assert result["clean_xml"] is None
        assert "XML Syntax Error" in result["validation_error"]

    def test_validate_xml_with_markdown_cleaning(self, test_state):
        """Test that validate_xml cleans markdown before validation"""
        invalid_xml = """```xml
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL">
    <bpmn:process id="Process_1" />
</bpmn:definitions>
```"""
        test_state["xml_content"] = invalid_xml

        result = validate_xml(test_state)

        assert result["is_valid"] is True
        assert result["clean_xml"] is not None
        # Verify markdown was stripped
        assert "```xml" not in result["clean_xml"]
        assert result["clean_xml"].startswith("<bpmn:definitions")

    def test_validate_xml_empty_content(self, test_state):
        """Test validation fails for empty content"""
        test_state["xml_content"] = ""

        result = validate_xml(test_state)

        assert result["is_valid"] is False
        assert result["clean_xml"] is None
        assert result["validation_error"] is not None

    def test_validate_xml_malformed_entities(self, test_state):
        """Test validation fails for malformed entities"""

        test_state["xml_content"] = "<test>&invalid_entity;</test>"

        result = validate_xml(test_state)

        assert result["is_valid"] is False
        assert result["clean_xml"] is None
        assert result["validation_error"] is not None

    def test_validate_xml_preserves_thread_id_in_log(self, test_state, caplog):
        """Test that thread_id is used in logging (verified via no exceptions)"""
        test_state["thread_id"] = "specific-thread-id-12345"

        validate_xml(test_state)

        with caplog.at_level(logging.INFO):
            assert "specific-thread-id-12345" in caplog.text

    def test_validate_xml_with_namespaces(self, test_state):
        """Test validation of XML with various namespaces"""
        test_state[
            "xml_content"
        ] = """<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
                 xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
                 xmlns:di="http://www.omg.org/spec/DD/20100524/DI">
    <bpmn:process id="Process_1" isExecutable="true">
        <bpmn:startEvent id="StartEvent_1" name="Start">
            <bpmn:outgoing>Flow_1</bpmn:outgoing>
        </bpmn:startEvent>
        <bpmn:task id="Task_1" name="Do Something">
            <bpmn:incoming>Flow_1</bpmn:incoming>
            <bpmn:outgoing>Flow_2</bpmn:outgoing>
        </bpmn:task>
        <bpmn:endEvent id="EndEvent_1" name="End">
            <bpmn:incoming>Flow_2</bpmn:incoming>
        </bpmn:endEvent>
        <bpmn:sequenceFlow id="Flow_1" sourceRef="StartEvent_1" targetRef="Task_1" />
        <bpmn:sequenceFlow id="Flow_2" sourceRef="Task_1" targetRef="EndEvent_1" />
    </bpmn:process>
</bpmn:definitions>"""

        result = validate_xml(test_state)

        assert result["is_valid"] is True
        assert result["clean_xml"] is not None
        assert "StartEvent_1" in result["clean_xml"]
        assert "Task_1" in result["clean_xml"]
