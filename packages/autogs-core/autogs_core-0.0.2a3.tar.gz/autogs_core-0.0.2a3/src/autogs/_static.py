import os
import warnings

from dotenv import load_dotenv

load_dotenv()


def get_env_var(var_name: str) -> str:
    var = os.getenv(var_name)
    if not var:
        warnings.warn(
            f"Environment variable {var_name} not found. Defaulting to empty string. "
            f"If this is not the desired behavior, please set the environment variable."
            f"For example set {var_name} = <...>, in a .env file in the root of the project."
        )
    return os.getenv(var_name) or ""


# PROJECT
DEFAULT_PROJECT = get_env_var("MY_DEFAULT_PROJECT")

DEFAULT_LOCATION = get_env_var("MY_LOCATION")
DEFAULT_MODEL = get_env_var("MY_MODEL")

DEFAULT_PROCESSOR_LOCATION = get_env_var("MY_PROCESSOR_LOCATION")
DEFAULT_ORC_PROCESSOR = get_env_var("MY_ORC_PROCESSOR")

DEFAULT_GITHUB_TOKEN = get_env_var("MY_GITHUB_TOKEN")
