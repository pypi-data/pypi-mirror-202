import json
import os
import wave
import zipfile
from dataclasses import dataclass
from pathlib import Path
from urllib import request

import numpy as np
from pydantic import AnyUrl
from vosk import KaldiRecognizer, SpkModel, Model

from jarvis.config.vosk import VOSK
from jarvis.whisper.inputs import StreamInput, FileInput


@dataclass
class VoskModelDownloader:
    model_url: AnyUrl = f'{VOSK.download_url}/{VOSK.model_name}'
    spk_model_url: AnyUrl = f'{VOSK.download_url}/{VOSK.spk_model_name}'

    # FIXME: Download all
    models_mapping: tuple[tuple[str, AnyUrl]] = (
        (
            VOSK.model_name, f'{VOSK.download_url}/{VOSK.model_name}.zip'
        ),
        (
            VOSK.spk_model_name, f'{VOSK.download_url}/{VOSK.spk_model_name}.zip'
        )
    )

    @classmethod
    def download_models(cls):
        for model_item in cls.models_mapping:

            if not os.path.exists(VOSK.models_path):
                os.mkdir(VOSK.models_path)
            zip_file_path: Path = Path(f'{VOSK.models_path}/{model_item[0]}.zip')
            if not os.path.exists(str(zip_file_path)[:-4]):
                request.urlretrieve(model_item[1], zip_file_path)
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(VOSK.models_path)
                os.remove(zip_file_path)


@dataclass
class VoskSpeakerIdentifier:

    @staticmethod
    def __cosine_dist(x: list[float], y: list[float]) -> float:
        nx = np.array(x)
        ny = np.array(y)
        return 1 - np.dot(nx, ny) / np.linalg.norm(nx) / np.linalg.norm(ny)

    @classmethod
    def get_voice_spk(
            cls,
            input_: FileInput | StreamInput
    ) -> list[float]:
        model = Model(lang=VOSK.language)
        spk_model = SpkModel(f'{VOSK.models_path}\\{VOSK.spk_model_name}')
        wf = wave.open(input_.path)
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetSpkModel(spk_model)
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            rec.AcceptWaveform(data)

        res = json.loads(rec.FinalResult())
        return res['spk']

    @classmethod
    def identify(
            cls,
            input_: FileInput | StreamInput,
            spk_verifier: list[float]
    ) -> bool:
        if cls.__cosine_dist(cls.get_voice_spk(input_), spk_verifier) < VOSK.identify_gate:
            return True
        return False


@dataclass
class VoskSpeaker:
    ...
