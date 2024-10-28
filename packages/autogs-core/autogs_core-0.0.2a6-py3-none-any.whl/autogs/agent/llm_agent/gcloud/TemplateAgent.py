import vertexai
from jinja2 import Template
from vertexai.generative_models import GenerativeModel

from autogs._static import DEFAULT_LOCATION, DEFAULT_MODEL, DEFAULT_PROJECT
from autogs.agent.llm_agent.gcloud._static import GENERATION, SAFETY


class TemplateAgent:
    """
    Agent that uses a jinja2 template to generate
    """

    def __init__(
        self,
        template_file,
        project: str = DEFAULT_PROJECT,
        location: str = DEFAULT_LOCATION,
        model: str = DEFAULT_MODEL,
    ):
        vertexai.init(project=project, location=location)
        self.model = GenerativeModel(model)

        with open(template_file, "r") as file:
            _content = file.read()
            self.template = Template(_content)

    def render(self, **kwargs):
        return self.template.render(**kwargs)

    def generate(self, **kwargs):
        responses = self.model.generate_content(
            [f"""{self.render(**kwargs)}"""],
            generation_config=GENERATION,
            safety_settings=SAFETY,
            stream=True,
        )
        return "".join([r.text for r in responses])
