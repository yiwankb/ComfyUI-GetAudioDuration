from ._types import AUDIO


class ComfyUI_GetAudioDuration:
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


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "ComfyUI_GetAudioDuration": ComfyUI_GetAudioDuration
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI_GetAudioDuration": "ComfyUI-GetAudioDuration"
}