import os
from dataclasses import dataclass

import torch

from jarvis.config.silero import SILERO

device = torch.device('cpu')
torch.set_num_threads(4)


@dataclass
class SileroModelDownloader:

    @classmethod
    def download_models(cls):
        if not os.path.isfile(SILERO.model_name):
            torch.hub.download_url_to_file(SILERO.model_download_url, SILERO.model_name)


@dataclass
class SileroSpeakerIdentifier:
    ...


@dataclass
class SileroSpeaker:
    ...


# model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
# model.to(device)

# example_text = 'Привет! Меня зовут Джарвис'
# sample_rate = 48000
# speaker = 'baya'
#
# audio_paths = model.save_wav(text=example_text,
#                              speaker=speaker,
#                              sample_rate=sample_rate)
