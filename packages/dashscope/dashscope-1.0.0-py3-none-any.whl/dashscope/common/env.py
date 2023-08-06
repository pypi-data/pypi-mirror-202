import os

from dashscope.common.constants import (DASHSCOPE_API_KEY_ENV,
                                        DASHSCOPE_API_KEY_FILE_PATH_ENV,
                                        DASHSCOPE_API_REGION_ENV,
                                        DASHSCOPE_API_VERSION_ENV)

api_region = os.environ.get(DASHSCOPE_API_REGION_ENV, 'cn-beijing')
api_version = os.environ.get(DASHSCOPE_API_VERSION_ENV, 'v1')
# read the api key from env
api_key = os.environ.get(DASHSCOPE_API_KEY_ENV)
api_key_file_path = os.environ.get(DASHSCOPE_API_KEY_FILE_PATH_ENV)

# define api base url, ensure end /
base_http_api_url = os.environ.get(
    'DASHSCOPE_HTTP_BASE_URL',
    'https://dashscope-%s.aliyun-inc.com/api/%s' % (api_region, api_version))
base_websocket_api_url = os.environ.get(
    'DASHSCOPE_WEBSOCKET_BASE_URL',
    'wss://dashscope-%s.aliyun-inc.com/api-ws/%s/inference' %
    (api_region, api_version))
