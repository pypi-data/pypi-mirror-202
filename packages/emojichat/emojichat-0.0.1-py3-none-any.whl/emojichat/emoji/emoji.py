from typing import Optional

from emojichat.gpt import ChatGPT
from emojichat.prompts import EmojiPrompt


def emojize(
    content: str,
    model: str = "gpt-3.5-turbo",
    api_key: Optional[str] = None,
    **kwargs
) -> str:
    r"""Emojize a paragraph by using ChatGPT
    to generate emojis from text.

    Parameters
    ----------
    content: str
        Content to be emojized.
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
    >>> content = "I am ok in the morning, but feel bad at night."
    >>> emojize(content, temperature=0)
    🙂🌅➡️😔🌃
    """
    prompt_generator = EmojiPrompt()
    prompt = prompt_generator.generate_prompt(content)
    gpt = ChatGPT(api_key=api_key)
    response = gpt.get_chat_response(prompt, model, **kwargs)
    return gpt.get_response_message(response)
