from pydantic import BaseSettings


class SoundSettings(BaseSettings):
    device_index: int | None = None
    energy_threshold: int = 500
    sample_rate: int = 44100
    ggts_language: str = 'ru'
    stop_words: set[str] = {'', }

    class Config:
        env_prefix = 'SOUND_'


SOUND: SoundSettings = SoundSettings()
