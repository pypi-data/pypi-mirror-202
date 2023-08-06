from os.path import dirname

from neon_transformers import AudioTransformer
from neon_transformers.tasks import AudioTask
from precise_lite_runner.runner import Listener


class SpeakerGenderClassifier(AudioTransformer):
    task = AudioTask.ADD_CONTEXT

    def __init__(self, config=None):
        config = config or {}
        super().__init__("speaker_gender", 10, config)
        model = config.get("model") or f"{dirname(__file__)}/male_ww.tflite"
        self.thresh = config.get("thresh", 0.4)  # sensitivity, higher -> more likely to classify female
        self.clf = Listener(model)

    # HACK: fixing bug in neon-transformers
    def feed_speech_chunk(self, chunk):
        chunk = self.on_speech(chunk)  # <- typo in neon
        self.speech_feed.write(chunk)

    # plugin api
    def transform(self, audio_data):
        speech = self.speech_feed.read()
        prob = self.clf.get_prediction(speech)
        if prob >= self.thresh:
            gender = "male"
        else:
            gender = "female"
        return audio_data, {"speaker_gender": gender}


def create_module(config=None):
    return SpeakerGenderClassifier(config=config)
