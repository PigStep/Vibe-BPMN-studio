from typing import Literal
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

    def get_prompt(
        self,
        prompt_name: str,
        prompt_type: Literal["system", "user"] = "user",
        **kwargs,
    ) -> str | None:
        """
        Retrieves and renders a prompt template from a YAML file.

        Parameters
        ----------
        promt_name : str
            The base name of the prompt file (without extension) located in
            ``self.prompt_dir``.
        prompt_type : Literal["system", "user"], optional
            The type of template to load.  The YAML file must contain a
            ``templates`` mapping with keys ``system`` and ``user``.  Defaults
            to ``"user"``.
        **kwargs
            Keyword arguments that will be passed to the Jinja2 template
            renderer.  These correspond to the variables used inside the
            template.

        Returns
        -------
        str | None
            The rendered prompt string if the file and template were
            successfully loaded and rendered.  Returns ``None`` if the file
            does not exist, cannot be parsed, or the requested template type
            is missing.
        """
        file_path = self.prompt_dir / f"{prompt_name}.yaml"

        data = self._load_yaml(file_path)

        try:
            raw_template = data["templates"][prompt_type]
        except KeyError:
            logger.error(f"Missing template type for {prompt_name}")
            return None

        template = Template(raw_template)
        return template.render(**kwargs)

    @staticmethod
    @lru_cache(maxsize=32)
    def _load_yaml(file_path: Path) -> dict:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file) or {}
        except Exception as e:
            logger.error(f"Failed to load YAML at {file_path}: {e}")
            return {}


manager = PromptManager()


def get_prompt_manager() -> PromptManager:
    return manager
