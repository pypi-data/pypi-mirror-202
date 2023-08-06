<h4 align="center">
    <p>
        <b>English</b> |
        <a href="https://github.com/dashscope/dashscope/blob/master/README_zh.md">中文</a>
    <p>
</h4>


</div>

# DashScope Python Library

## Installation
To install the DashScope Python SDK, simply run:
```shell
pip install dashscope
```

If you clone the code from github, you can install from  source by running:
```shell
pip install -e .
```



## QuickStart

You can use `Conversation` api to directly chat with model qwen-v1(通义千问).

```python
import dashscope
from dashscope import Conversation

dashscope.api_key = '12344343222194ADSSDSSDSDSB9A511ED830AFA4166304A26'

def stream_print(responses):
    for r in responses:
        if r.status_code == 200:
            print(r.output.text.replace('\n', '  '), end='\r')
            print(r.usage)
        else:
            print(r.message)

chat = Conversation()

responses = chat.call('qwen-v1',
    prompt='以松柏为题，写一首七言诗。',
    stream=True)
stream_print(responses)

responses = chat.call('qwen-v1',
    prompt='现在假设你是一名精通中英双语的学者，将上面这首诗翻译成英文。',
    stream=True)
stream_print(responses)

```

## API Key Authentication

The SDK uses API key authentication. [Get your API key here](https://aliyuque.antfin.com/zztrg2/zl1nqe/qo56foez7a2hgwyk).

### Using the API Key

1. Set the API key via code
```python
import dashscope

dashscope.api_key = 'your-api-key'
# Or specify the API key file path via code
# dashscope.api_key_file_path='~/.dashscope/api_key'

```

2. Set the API key via environment variables

a. Set the API key directly using the environment variable below

```python
export DASHSCOPE_API_KEY='your_api_key'
```

b. Specify the API key file path via an environment variable

```python
export DASHSCOPE_API_KEY_FILE_PATH='~/.dashscope/api_key'
```

3. Save the API key to a file
```python
from dashscope import save_api_key

save_api_key(api_key='your_api_key',
             api_key_file_path='api_key_file_location or (None, will save to default location "~/.dashscope/api_key"')

```


## Sample Code

`call` function provides  synchronous call, the function call will return when the whole computing process finish on the server side.

```python
from http import HTTPStatus
from dashscope import Generation
# export DASHSCOPE_API_KEY='your_api_key' in environment
def sync_dashscope_sample():
    responses = Generation.call(
        model=Generation.Models.qwen_v1,
        prompt='Is the weather good today?')

    if responses.status_code == HTTPStatus.OK:
        print('Result is: %s'%responses.output)
    else:
        print('Code: %s, status_code: %s, code: %s, message: %s'%(responses.status_code,
                                                   responses.code,
                                                   responses.message))

if __name__ == '__main__':
    sync_dashscope_sample()
```

For requests with longer processing times, you can obtain partial results before the full output is generated. Set the **stream** parameter to **True**. In this case, the results will be returned in batches, and the current output mode is incremental (output will overwrite the previous content). When the output is in stream mode, the interface returns a generator, and you need to iterate through the generator to get the results. Each output contains partial data for streaming, and the last output contains the final generated result.

Example with simple streaming:
```python
from http import HTTPStatus
from dashscope import Generation

def sample_sync_call_stream():
    prompt_text = 'Give me a recipe using carrots, potatoes, and eggplants'
    response_generator = Generation.call(
        model=Generation.Models.qwen_v1,
        prompt=prompt_text,
        stream=True,
        max_length=512,
        top_k=15)
    for resp in response_generator:  # Iterate through the streaming output results
        if resp.status_code == HTTPStatus.OK:
            print(resp.output)
        else:
            print('Request failed, message: %s'%resp.message)

if __name__ == '__main__':
    sample_sync_call_stream()

```
#### Streaming with History
```python
from http import HTTPStatus

from dashscope import Conversation, History, HistoryItem
def conversation_stream_example():
    history = History()
    item = HistoryItem('user', text='Is the weather good today?')
    history.append(item)
    item = HistoryItem('bot', text='The weather is nice today, do you want to go out and play?')
    history.append(item)

    item = HistoryItem('user', text='Do you have any places to recommend?')
    history.append(item)
    item = HistoryItem('bot', text='I suggest you go to the park. Spring is here, and the flowers are blooming. It is beautiful.')
    history.append(item)
    chat = Conversation(history)
    response = chat.call(Conversation.Models.qwen_v1,
                         prompt='Recommend a nearby park',
                         stream=True)
    for part in response:
        if part.status_code == HTTPStatus.OK:
            print(part.output)
        else:
            print('Failed request_id: %s, status_code: %s code: %s, message:%s' %
                  (part.id, part.status_code, part.code, part.message))
    response = chat.call(
        Conversation.Models.qwen_v1,
        prompt='I have been to that park many times, how about a more distant one?',
        auto_history=True,
        stream=True,
    )
    for part in response:
        if part.status_code == HTTPStatus.OK:
            print(part.output.text)
            print(part.usage)
        else:
            print('Failed request_id: %s, status_code: %s, code: %s, message:%s' %
                  (part.id, part.status_code, part.code, part.message))


if __name__ == '__main__':
    conversation_stream_example()


```
## Logging
To output Dashscope logs, you need to configure the logger.
```python
    import logging

    logger = logging.getLogger('dashscope')
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # add console_handler to logger
    logger.addHandler(console_handler)

```

## Output
The output contains the following fields:
```
     request_id (str): The request id.
     status_code (int): HTTP status code, 200 indicates that the
         request was successful, others indicate an error。
     code (str): Error code if error occurs, otherwise empty str.
     message (str): Set to error message on error.
     output (Any): The request output.
     usage (Any): The request usage information.
```

## Error Handling
Currently, errors are thrown as exceptions.


## Contributing
We welcome contributions to the DashScope Python SDK! To contribute, please follow these steps:

Fork the repository on GitHub.
Create a new branch for your changes.
Implement your changes and add tests.
Make sure all tests pass by running pytest.
Submit a pull request to the main branch.
For more information on contributing, please read our contributing guidelines.

## License
This project is licensed under the [Apache License (Version 2.0)](https://github.com/dashscope/dashscope/blob/master/LICENSE).
