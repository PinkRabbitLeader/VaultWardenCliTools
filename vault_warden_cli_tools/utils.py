__all__ = ["detect_os", "extract_date", "add_to_path"]

import os
import platform
import sys


def detect_os() -> str:
    from vault_warden_cli_tools.exceptions import UnsupportedOSError
    """
    检测并返回操作系统名称。
    支持的操作系统包括: Windows, Linux, macOS。
    """
    # 获取操作系统名称
    os_name = _os_name.lower() if (_os_name := platform.system()) != "Darwin" else "macos"
    if os_name != "windows" and os_name != "linux" and os_name != "macos":
        raise UnsupportedOSError(f"不支持的操作系统: {os_name}")
    else:
        return os_name


# 定义一个函数来从文件名中提取日期信息
def extract_date(filename) -> str:
    parts = filename.split('-')
    for part in parts:
        if part.count('.') == 2 and all(char.isdigit() or char == '.' for char in part):
            return part

    # 如果没有有效日期信息，返回文件名本身
    return filename


def add_to_path(new_directory):
    """
    根据操作系统自动将新目录添加到 PATH 环境变量中。
    仅在当前 Python 会话中生效。
    """
    current_path = os.environ.get('PATH', '')
    if sys.platform.startswith('win'):
        # Windows 平台
        os.environ['PATH'] = f"{current_path};{new_directory}"
    else:
        # Linux 或 macOS 平台
        os.environ['PATH'] = f"{current_path}:{new_directory}"
