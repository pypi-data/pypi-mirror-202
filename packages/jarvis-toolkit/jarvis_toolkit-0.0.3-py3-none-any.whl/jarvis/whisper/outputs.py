from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment

from jarvis.config.sound import SOUND
from jarvis.gpt.context import ContextHandler


class StreamOutput:

    @classmethod
    def transform(cls, context_handler: ContextHandler) -> AudioSegment:
        fp = BytesIO()
        gTTS(
            text=context_handler.last_answer,
            lang=SOUND.ggts_language,
            tld='com',
            slow=False
        ).write_to_fp(fp)
        fp.seek(0)
        segment = AudioSegment.from_file(fp, 'mp3')
        fp.close()
        return segment


class FileOutput:
    pass
