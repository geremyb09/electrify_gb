import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from config import PROMPTS_DIR


class PromptManager:
    """Manages loading and rendering of Jinja2 prompt templates"""

    def __init__(self, templates_dir: str = PROMPTS_DIR):
        """
        Initialize the prompt manager.

        Args:
            templates_dir: Directory containing Jinja2 templates
        """
        os.makedirs(templates_dir, exist_ok=True)

        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, template_name: str, **kwargs) -> str:
        """
        Render a Jinja2 template with provided variables.

        Args:
            template_name: Name of the template file
            **kwargs: Variables to pass to the template

        Returns:
            Rendered prompt string
        """
        template = self.env.get_template(template_name)
        return template.render(**kwargs)


prompt_manager = PromptManager()
