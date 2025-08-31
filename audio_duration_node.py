from pydub import AudioSegment
from .base_node import BaseNode

class ComfyUI_GetAudioDuration(BaseNode):
    """
    A ComfyUI node to calculate the duration of an audio file.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio_file": ("AUDIO", {"default": None}),
            },
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("duration",)
    FUNCTION = "calculate_duration"
    CATEGORY = "ComfyUI-GetAudioDuration"

    def calculate_duration(self, audio_file):
        """
        Calculate the duration of the audio file in seconds.
        """
        if audio_file is None:
            raise ValueError("Audio file is not provided.")

        duration_seconds = len(audio_file) / 1000.0  # Convert milliseconds to seconds
        return (duration_seconds,)

