import speech_recognition as sr


from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Literal, BinaryIO, Generator
from pydub import AudioSegment

from jarvis.config.sound import SOUND


@dataclass
class FileInput:
    path: Path | str
    format: Literal['mp3', 'wav', 'm4a'] = 'm4a'
    _cur_stream: BinaryIO = None

    def read(self) -> BinaryIO:
        self._cur_stream = open(self.path, 'rb')
        return self._cur_stream

    def __enter__(self):
        return self.read()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._cur_stream.close()


@dataclass
class StreamInput:
    tmp_file_path: Path = Path('./temp_file.wav')
    tmp_file_format: Literal['mp3', 'wav', 'm4a'] = 'wav'
    stop_listen: bool = False
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = SOUND.energy_threshold
    recognizer.pause_threshold = 1

    def read(self, audio_data: sr.AudioData | BytesIO) -> FileInput:
        if isinstance(audio_data, sr.AudioData):
            audio_clip = AudioSegment.from_file(BytesIO(audio_data.get_wav_data()), format=self.tmp_file_format)
        elif isinstance(audio_data, BytesIO):
            audio_clip = AudioSegment.from_file(audio_data, format=self.tmp_file_format)
        else:
            raise ValueError
        audio_clip.export(self.tmp_file_path, format=self.tmp_file_format)
        return FileInput(path=self.tmp_file_path, format=self.tmp_file_format)

    def read_from_stream(self) -> Generator[FileInput, None, None]:
        with sr.Microphone(
                device_index=SOUND.device_index,
                sample_rate=SOUND.sample_rate
        ) as source:
            self.recognizer.adjust_for_ambient_noise(source, 1)
            while 1:
                yield self.read(self.recognizer.listen(source))
                if self.stop_listen:
                    break

    def record_from_stream(self, duration: int) -> FileInput:

        with sr.Microphone(
                device_index=SOUND.device_index,
                sample_rate=SOUND.sample_rate
        ) as source:
            self.recognizer.adjust_for_ambient_noise(source, 1)
            return self.read(self.recognizer.record(source=source, duration=duration))
