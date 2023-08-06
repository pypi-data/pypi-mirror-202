from pydantic import BaseSettings, AnyUrl


class SileroSettings(BaseSettings):
    """
        https://models.silero.ai/models/tts/ru/v3_1_ru.pt
    """
    download_url: AnyUrl = 'https://models.silero.ai/models/tts'
    language: str = 'ru'
    model_name: str = 'v3_1_ru.pt'

    class Config:
        env_prefix = 'SILERO_'

    @property
    def model_download_url(self):
        return '/'.join((self.download_url, self.language, self.model_name))


SILERO: SileroSettings = SileroSettings()
