from typing import Optional, Text


def setup_openai_api_key(
    organization_id: Optional[Text] = None,
    api_key: Optional[Text] = None,
    api_base: Optional[Text] = None,
    api_type: Optional[Text] = None,
    api_version: Optional[Text] = None,
):
    """Setup the OpenAI API key.

    Parameters
    ----------
    organization_id : Optional[Text]
        The organization id.
    api_key : Optional[Text]
        The API key.
    api_base : Optional[Text]
        The API base.
    api_type : Optional[Text]
        The API type.
    api_version : Optional[Text]
        The API version.
    """

    try:
        import openai
    except ImportError:
        raise ImportError(
            "Openai is not installed. Please install it by `pip install openai`."
        )

    if organization_id:
        openai.organization = organization_id
    if api_key:
        openai.api_key = api_key
    if api_base:
        openai.api_base = api_base
    if api_type:
        openai.api_type = api_type
    if api_version:
        openai.api_version = api_version
