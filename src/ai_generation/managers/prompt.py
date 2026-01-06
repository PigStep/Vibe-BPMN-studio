import yaml
from jinja2 import Template
from pathlib import Path
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)


class PromptManager:
    """Manages loading and rendering prompt templates from YAML files."""

    def __init__(self, prompt_dir: str = r"data/prompts"):
        self.prompt_dir = Path(prompt_dir)

    def get_call_config(
        self,
        prompt_name: str,
        **kwargs,
    ) -> dict:
        """
        Retrieves and renders a prompt template from a YAML file.

        Parameters
        ----------
        promt_name : str
            The base name of the prompt file (without extension) located in
            ``self.prompt_dir``.
        **kwargs
            Keyword arguments that will be passed to the Jinja2 template
            renderer.  These correspond to the variables used inside the
            template.

        Returns
        -------
        dict
            The rendered llm call configuration if the file and template were
            successfully loaded and rendered.
        """
        file_path = self.prompt_dir / f"{prompt_name}.yaml"

        raw_data = self._load_file(file_path)
        filled_data = self._render_yaml(raw_data, **kwargs)
        return self._parse_yaml(filled_data)

    @staticmethod
    @lru_cache(maxsize=32)
    def _load_file(file_path: Path) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception:
            logger.error("Failed to load file at %s", file_path)
            return ""

    @staticmethod
    def _parse_yaml(data: str) -> dict:
        try:
            return yaml.safe_load(data) or {}
        except Exception as e:
            logger.error("Failed to load YAML: %s", e)
            return {}

    @staticmethod
    def _render_yaml(data: str, **kwargs) -> dict:
        """
        Render a YAML dict as a Jinja2 template.

        """
        template = Template(data)
        return template.render(**kwargs)


manager = PromptManager()


def get_basic_prompt_manager() -> PromptManager:
    return manager
