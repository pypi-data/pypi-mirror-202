from typing import Any, Generator, Union

from dashscope.api_entities.dashscope_response import GenerationResponse
from dashscope.client.base_api import BaseApi
from dashscope.common.constants import HISTORY, PROMPT
from dashscope.common.error import InputRequired
from dashscope.common.utils import _get_task_group_and_task


class Generation(BaseApi):
    task = 'text-generation'
    """API for AI-Generated Content(AIGC) models.

    """
    class Models:
        qwen_v1 = 'qwen-v1'

    @classmethod
    def call(
        cls,
        model: str,
        prompt: Any,
        history: list = None,
        api_key: str = None,
        **kwargs
    ) -> Union[GenerationResponse, Generator[GenerationResponse, None, None]]:
        """Call generation model service.

        Args:
            model (str): The requested model, such as gpt3-v2
            prompt (Any): The input prompt.
            history (list):The user provided history,
                examples:
                    [{'user':'The weather is fine today.',
                    'bot': 'Suitable for outings'}].
                Defaults to None.
            api_key (str, optional): The api api_key, can be None,
                if None, will get by default rule(TODO: api key doc).
            **kwargs(qwen-v1, qawen-plus-v1):
                stream(bool, `optional`): Enable server-sent events
                    (ref: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)  # noqa E501
                    the result will back partially.
                max_length(int, `optional`): The maximum length of tokens to
                    generate. The token count of your prompt plus max_length
                    cannot exceed the model's context length. Most models
                    have a context length of 2000 tokens.
                top_p(int, `optional`): A sampling strategy, called nucleus
                    sampling, where the model considers the results of the
                    tokens with top_p probability mass. So 0.1 means only
                    the tokens comprising the top 10% probability mass are
                    considered.
                enable_search(bool, `optional`): Whether to enable web search(quark).  # noqa E501
                    Currently works best only on the first round of conversation.
                    Default to False.

        Raises:
            InvalidInput: The history and auto_history are mutually exclusive.

        Returns:
            Union[GenerationResponse,
                  Generator[GenerationResponse, None, None]]: If
            stream is True, return Generator, otherwise GenerationResponse.
        """
        if prompt is None or not prompt:
            raise InputRequired('prompt is required!')
        task_group, function = _get_task_group_and_task(__name__)
        enable_search = kwargs.pop('enable_search', False)
        M6_NUM_WEB_SEARCH = 0
        M6_SEARCH_IN_FIRST_QUERY = 0
        if enable_search:
            M6_NUM_WEB_SEARCH = 5
            M6_SEARCH_IN_FIRST_QUERY = 0
        response = super().call(
            model=model,
            task_group=task_group,
            task=Generation.task,
            function=function,
            api_key=api_key,
            input={
                PROMPT: prompt,
                HISTORY: history if history else [],
            },
            M6_NUM_WEB_SEARCH=M6_NUM_WEB_SEARCH,
            M6_SEARCH_IN_FIRST_QUERY=M6_SEARCH_IN_FIRST_QUERY,
            **kwargs)
        is_stream = kwargs.get('stream', False)
        if is_stream:
            return (GenerationResponse.from_api_response(rsp)
                    for rsp in response)
        else:
            return GenerationResponse.from_api_response(response)
