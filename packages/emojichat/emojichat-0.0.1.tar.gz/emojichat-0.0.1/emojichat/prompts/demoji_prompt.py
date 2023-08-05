from typing import Optional

from emojichat.typing import MESSAGE, PROMPT


class DemojiPrompt:
    r"""Prompt class for demoji.

    Parameters
    ----------
    train_prompt: PROMPT, optional (default: :obj:`None`)
        Prompt that will be put before the question.
        If not specified, will be automatically generated.
    """

    def __init__(self, train_prompt: Optional[PROMPT] = None):
        if train_prompt is None:
            train_prompt = self.get_train_prompt()
        self.train_prompt = train_prompt

    def generate_prompt(self, content: str) -> PROMPT:
        r"""Generate final prompt.

        Parameters
        ----------
        content: str
            Content to be demojized.

        Returns
        -------
        prompt: PROMPT
            Prompt to be put into the model.
        """
        prmopt = [self._generate_system_message()]
        question = {"role": "user", "content": content}
        return prmopt + self.train_prompt + [question]

    def _generate_system_message(self) -> MESSAGE:
        content = (
            "Can you write some sentence based on following emoji? "
            "Please just return the final sentence and not include "
            "any emoji or other response."
        )
        message = {"role": "system", "content": content}
        return message

    def get_train_prompt(self) -> PROMPT:
        r"""Generate the train prompt.

        Returns
        -------
        train_prompt: PROMPT
            Train prompt.
        """
        prompt = []
        # conjunction
        conj_prompt = []
        question = {"role": "user", "content": "😃🌅↩️😔🌆"}
        answer = {
            "role": "assistant",
            "content": (
                "I am very happy in the morning, "
                "but become sad in the afternoon."
            ),
        }
        conj_prompt.extend([question, answer])
        question = {"role": "user", "content": "🙂🌅➡️😃🌃"}
        answer = {
            "role": "assistant",
            "content": "I am ok in the morning and very happy in the evening.",
        }
        conj_prompt.extend([question, answer])
        question = {"role": "user", "content": "🍎👍️➡️🍊❤️"}
        answer = {
            "role": "assistant",
            "content": (
                "I am very happy in the morning, "
                "but become sad in the afternoon."
            ),
        }
        conj_prompt.extend([question, answer])
        prompt += conj_prompt
        return prompt
