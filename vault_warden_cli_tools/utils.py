__all__ = ["detect_os", "extract_date"]

import platform

from vault_warden_cli_tools.exceptions import UnsupportedOSError


def detect_os() -> str:
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
