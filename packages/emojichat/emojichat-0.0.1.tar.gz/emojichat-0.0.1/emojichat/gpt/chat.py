from typing import Any, Optional

from emojichat.typing import PROMPT


class ChatGPT:
    r"""A wrapper class to :class:`openai.ChatCompletion`.

    Parameters
    ----------
    api_key: str, optional (default: :obj:`None`)
        API key to be used as `openai.api_key`.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
    ):
        self.api_key = api_key

    def get_chat_response(
        self, prompt: PROMPT, model: str = "gpt-3.5-turbo", **kwargs
    ) -> Any:
        r"""Put prompt to the model and get response.

        Parameters
        ----------
        prompt: PROMPT
            Prompt to be put into the chat model.
        model: str, default: :obj:`gpt-3.5-turbo`
            Underlying GPT model.
        kwargs: Any
            Other optional parameters to be used in the chat model,
            such as :obj:`temperature`.

        Returns
        -------
        response: Any
            Response from the ChatGPT model.
        """
        import openai

        if openai.api_key is None:
            openai.api_key = self.api_key

        temperature = kwargs.get("temperature", 1)

        response = openai.ChatCompletion.create(
            model=model,
            messages=prompt,
            temperature=temperature,
        )
        return response

    def get_response_message(self, response: Any) -> str:
        r"""Get response content.

        Parameters
        ----------
        response: Any
            Response from the ChatGPT model.

        Returns
        -------
        content: str
            Content from model response.
        """
        return response.choices[0]["message"]["content"]
