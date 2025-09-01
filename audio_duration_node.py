import torch
from typing import Tuple, Dict, Any


class AudioDurationNode:
    """
    音频时长计算节点
    输入AUDIO类型，输出该音频的时长（秒数）
    """

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "audio": ("AUDIO",),
            },
        }

    RETURN_TYPES = ("FLOAT", "STRING", "INT")
    RETURN_NAMES = ("duration_seconds", "formatted_time", "duration_ms")
    FUNCTION = "calculate_audio_duration"
    CATEGORY = "audio/utils"
    DESCRIPTION = "计算音频的时长"
    OUTPUT_NODE = False

    def calculate_audio_duration(self, audio) -> Tuple[float, str, int]:
        """
        计算AUDIO类型的时长

        Args:
            audio: AUDIO类型（可能是Tensor或包含Tensor的字典）
        """

        if audio is None:
            raise ValueError("音频输入不能为空")

        # 提取音频张量和采样率
        audio_tensor, sample_rate = self._extract_audio_info(audio)

        if audio_tensor is None:
            raise ValueError("无法从AUDIO输入中提取有效的音频张量")

        # 获取音频形状信息
        original_shape = audio_tensor.shape

        # 处理不同的音频张量格式
        if len(original_shape) == 1:
            # [samples] -> 单声道
            num_samples = original_shape[0]
        elif len(original_shape) == 2:
            # [channels, samples]
            num_samples = original_shape[1]
        elif len(original_shape) == 3:
            # [batch, channels, samples] -> 标准格式
            num_samples = original_shape[2]
        else:
            raise ValueError(f"不支持的音频张量维度: {len(original_shape)}")

        # 计算时长
        duration_seconds = num_samples / sample_rate

        # 格式化时间输出 (HH:MM:SS.mmm)
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)
        milliseconds = int((duration_seconds - int(duration_seconds)) * 1000)

        formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        duration_ms = int(duration_seconds * 1000)

        # 输出信息
        print(f"音频时长计算 - 采样数: {num_samples}, 采样率: {sample_rate}Hz")
        print(f"时长: {formatted_time} ({duration_seconds:.3f}秒)")

        return (duration_seconds, formatted_time, duration_ms)

    def _extract_audio_info(self, audio):
        """从AUDIO类型中提取音频张量和采样率"""
        audio_tensor = None
        sample_rate = 44100  # 默认采样率

        if isinstance(audio, torch.Tensor):
            # 直接是Tensor
            audio_tensor = audio

        elif isinstance(audio, dict):
            # 字典结构，尝试提取音频张量
            possible_tensor_keys = ['samples', 'audio', 'data', 'waveform', 'tensor']

            for key in possible_tensor_keys:
                if key in audio and isinstance(audio[key], torch.Tensor):
                    audio_tensor = audio[key]
                    break

            # 如果没有找到常见键名，尝试找到第一个Tensor值
            if audio_tensor is None:
                for value in audio.values():
                    if isinstance(value, torch.Tensor):
                        audio_tensor = value
                        break

            # 尝试提取采样率
            possible_sr_keys = ['sample_rate', 'sampling_rate', 'sr', 'rate']
            for key in possible_sr_keys:
                if key in audio and isinstance(audio[key], (int, float)):
                    sample_rate = audio[key]
                    break

        return audio_tensor, sample_rate


class AudioSimpleDuration:
    """
    简化版音频时长计算（只输出秒数）
    """

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "audio": ("AUDIO",),
            },
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("duration_seconds",)
    FUNCTION = "calculate_simple_duration"
    CATEGORY = "audio/utils"
    DESCRIPTION = "计算音频时长（简化版）"

    def calculate_simple_duration(self, audio) -> Tuple[float]:
        """简化版时长计算"""
        if audio is None:
            raise ValueError("音频输入不能为空")

        audio_tensor, sample_rate = self._extract_audio_info(audio)

        if audio_tensor is None:
            raise ValueError("无法提取音频张量")

        shape = audio_tensor.shape
        if len(shape) == 3:
            num_samples = shape[2]
        elif len(shape) == 2:
            num_samples = shape[1]
        elif len(shape) == 1:
            num_samples = shape[0]
        else:
            raise ValueError(f"不支持的音频维度: {len(shape)}")

        duration_seconds = num_samples / sample_rate
        return (duration_seconds,)

    def _extract_audio_info(self, audio):
        """提取音频信息"""
        audio_tensor = None
        sample_rate = 44100

        if isinstance(audio, torch.Tensor):
            audio_tensor = audio
        elif isinstance(audio, dict):
            for key in ['samples', 'audio', 'data']:
                if key in audio and isinstance(audio[key], torch.Tensor):
                    audio_tensor = audio[key]
                    break

            for key in ['sample_rate', 'sampling_rate']:
                if key in audio and isinstance(audio[key], (int, float)):
                    sample_rate = audio[key]
                    break

        return audio_tensor, sample_rate


# 节点映射
NODE_CLASS_MAPPINGS = {
    "AudioDuration": AudioDurationNode,
    "AudioDurationSimple": AudioSimpleDuration,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AudioDuration": "🔊 Audio Duration",
    "AudioDurationSimple": "🔊 Audio Duration (Simple)",
}