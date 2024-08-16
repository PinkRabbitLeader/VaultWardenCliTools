import os

from vault_warden_cli_tools.bw_manager import update_bw, download_bw_tool
from vault_warden_cli_tools.utils import detect_os

# 定义包的版本号
version = "0.0.1"


def get_bw():
    """
    下载 Bitwarden CLI 工具，并设置相关环境变量。
    """
    try:
        os_name = detect_os()  # 获取当前操作系统名称
        # 获取 BW 工具
        bw_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bw_cli")
        bw_name = f"bw_windows.exe" if os_name == "windows" else f"bw_{os_name}"
        if not (os.path.exists(bw_path) and os.path.exists(os.path.join(bw_path, bw_name))):
            os.makedirs(bw_path, exist_ok=True)
            download_bw_tool(bw_name=bw_name, bw_path=bw_path)  # 下载 BW 工具

        os.environ['BITWARDENCLI_APPDATA_DIR'] = bw_path  # 设置环境变量指向 BW 工具目录
        print(f"BW 工具已配置成功，路径: {bw_path}")
    except Exception as e:
        print(f"获取 BW 工具时出现问题: {e}")


if not os.getenv('BITWARDENCLI_APPDATA_DIR', None):
    get_bw()
