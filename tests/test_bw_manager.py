import os

import pytest

from vault_warden_cli_tools.bw_manager import download_bw_tool


@pytest.mark.parametrize("os_name", ["windows", "linux", "macos"])
def test_download_bw_tool(os_name, mocker):
    # Mock detect_os 函数返回不同的操作系统名称
    mocker.patch('platform.system', return_value=os_name)

    # 获取 BW 工具路径
    bw_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bw_cli")

    # BW 工具完整地址路径
    bw_tool = download_bw_tool()

    assert os.path.exists(bw_tool) is True
