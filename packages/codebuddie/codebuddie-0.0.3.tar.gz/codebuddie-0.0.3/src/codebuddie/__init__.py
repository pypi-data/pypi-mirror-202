from codebuddie.code_updater import code_update # noqa
from codebuddie.exception_handler import OpenaiApiKeyException
from dotenv import load_dotenv
import os
import openai


class OpenAIAPIKeyManager:
    def __init__(self):
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        if self.OPENAI_API_KEY == "":
            message = "OpenAI API key is not set or not specified. \
                Set an environment variable OPENAI_API_KEY in your system. \
                    Refer to the documentation for more information."
            raise OpenaiApiKeyException(message=message)
        
_key_manager = OpenAIAPIKeyManager()
openai.api_key = _key_manager.OPENAI_API_KEY