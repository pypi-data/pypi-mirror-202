from typing import Literal

import openai
from pydantic import BaseSettings, SecretStr


class OpenAI(BaseSettings):
    secret_key: SecretStr
    model_engine: Literal[
        'text-davinci-003',
        'code-davinci-002',
        'gpt-3.5-turbo',
        'text-ada-001'
    ] = 'gpt-3.5-turbo'
    whisper_model: Literal['whisper-1'] = 'whisper-1'
    max_tokens_limit: int = 4000
    question_tokens_limit: int = 1000
    answer_tokens_limit: int = max_tokens_limit - question_tokens_limit
    answer_language: str = 'ru'
    calibration_message: str = f'You are a helpful sound assistant. Your name - jarvis Answer language: {answer_language}'

    class Config:
        env_prefix = 'OPEN_AI_'


OPEN_AI: OpenAI = OpenAI()

if not openai.api_key:
    openai.api_key = OPEN_AI.secret_key.get_secret_value()
