from pathlib import Path
from typing import Literal

from pydantic import BaseSettings, AnyUrl


class VoskSettings(BaseSettings):
    """
    https://alphacephei.com/vosk/models
    """
    models_path: Path
    model_name: str = 'vosk-model-small-ru-0.22'
    spk_model_name: str = 'vosk-model-spk-0.4'
    download_url: AnyUrl = 'https://alphacephei.com/vosk/models'
    language: Literal['ru', 'en'] = 'ru'
    identify_gate: float = 0.1

    class Config:
        env_prefix = 'VOSK_'


VOSK: VoskSettings = VoskSettings()
