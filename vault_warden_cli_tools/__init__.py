import os

from vault_warden_cli_tools.bw_manager import update_bw, download_bw_tool

# 定义包的版本号
version = "0.0.1"


def get_bw():
    """
    下载 Bitwarden CLI 工具，并设置相关环境变量。
    """
    bw_path = download_bw_tool()  # 下载 BW 工具
    os.environ['BITWARDENCLI_APPDATA_DIR'] = bw_path  # 设置环境变量指向 BW 工具目录


if not os.getenv('BITWARDENCLI_APPDATA_DIR', None):
    get_bw()
