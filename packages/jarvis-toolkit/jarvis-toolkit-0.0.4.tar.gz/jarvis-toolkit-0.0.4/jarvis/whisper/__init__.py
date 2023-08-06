from typing import Generator
from openai import Audio

from jarvis.config.openai import OPEN_AI
from jarvis.whisper.inputs import FileInput, StreamInput


class WhisperEngine:

    @classmethod
    def transcribe_from_file(cls, input_: FileInput) -> str:
        with input_ as io:
            return Audio.transcribe(OPEN_AI.whisper_model, io).text

    @classmethod
    def translate_from_file(cls, input_: FileInput) -> str:
        with input_ as io:
            return Audio.translate(OPEN_AI.whisper_model, io).text

    @classmethod
    def transcribe_from_stream(cls) -> Generator[str, None, None]:
        for chunk in StreamInput().read_from_stream():
            yield cls.transcribe_from_file(chunk)


    @classmethod
    def translate_from_stream(cls) -> Generator[str, None, None]:
        for chunk in StreamInput().read_from_stream():
            yield cls.translate_from_file(chunk)
