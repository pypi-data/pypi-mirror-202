from typing import Optional

from emojichat.gpt import ChatGPT
from emojichat.prompts import DemojiPrompt


def demojize(
    content: str,
    model: str = "gpt-3.5-turbo",
    api_key: Optional[str] = None,
    **kwargs
) -> str:
    r"""Demojize all emojis from a paragraph by using ChatGPT
    to generate content and replace all emojis.

    Parameters
    ----------
    content: str
        Content to be demojized.
    model: str, default: :obj:`gpt-3.5-turbo`
        Underlying GPT model.
    api_key: str, optional (default: :obj:`None`)
        API key to be used as `openai.api_key`.
    kwargs: Any
        Other optional parameters to be used in the chat model,
        such as :obj:`temperature`.

    Returns
    -------
    content: str
        Content from model response.

    Example
    -------
    >>> content = "I 🚴 last year in 🇨🇳"
    >>> demojize(content, temperature=0)
    I cycled last year in China.
    """
    prompt_generator = DemojiPrompt()
    prompt = prompt_generator.generate_prompt(content)
    gpt = ChatGPT(api_key=api_key)
    response = gpt.get_chat_response(prompt, model, **kwargs)
    return gpt.get_response_message(response)
