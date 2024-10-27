import vertexai
from vertexai.generative_models import GenerativeModel

from src.autogs._static import DEFAULT_LOCATION, DEFAULT_MODEL, DEFAULT_PROJECT
from src.autogs.agent.llm_agent._static import GENERATION, SAFETY


def generate(
    prompt: str,
    model: str = DEFAULT_MODEL,
    project: str = DEFAULT_PROJECT,
    location: str = DEFAULT_LOCATION,
):
    """
    Generate content from a prompt
    """
    vertexai.init(project=project, location=location)
    _model = GenerativeModel(
        model,
    )
    responses = _model.generate_content(
        [f"""{prompt}"""],
        generation_config=GENERATION,
        safety_settings=SAFETY,
        stream=True,
    )

    return "".join([r.text for r in responses])
