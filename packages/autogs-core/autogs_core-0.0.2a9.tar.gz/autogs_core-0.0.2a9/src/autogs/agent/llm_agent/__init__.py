"""

"""


def convert_to_bool(response: str) -> bool:
    """
    Convert a string response of an AI agent to a boolean
    """
    if response is None:
        return False
    if response.lower() in ["no", "false"]:
        return False
    if response.lower() in ["yes", "true"]:
        return True
    if (("yes" in response.lower() or "true" in response.lower()) and
            not ("no" in response.lower() or "false" in response.lower())):
        return True
    if (("no" in response.lower() or "false" in response.lower()) and
            not ("yes" in response.lower() or "true" in response.lower())):
        return False
    return False
