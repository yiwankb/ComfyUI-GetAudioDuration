from .audio_duration_node import ComfyUI_GetAudioDuration  # 从当前目录的 audio_duration_node.py 文件中导入 ComfyUI_GetAudioDuration 类

# 将节点类映射到名称
NODE_CLASS_MAPPINGS = {
    "ComfyUI_GetAudioDuration": ComfyUI_GetAudioDuration,  # "ComfyUI_GetAudioDuration" 是节点在系统中的内部标识符
}

# （可选）定义节点在UI中显示的更友好名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI_GetAudioDuration": "ComfyUI-GetAudioDuration",  # 这是在UI菜单中显示的名称
}

# 导出这些映射，以便 ComfyUI 发现
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']