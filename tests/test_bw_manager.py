import os

import pytest

from vault_warden_cli_tools.bw_manager import download_bw_tool


@pytest.mark.parametrize("os_name, expected_bw_name", [
    ("windows", "bw_windows.exe"),
    ("linux", "bw_linux"),
    ("macos", "bw_macos"),
])
def test_download_bw_tool(os_name, expected_bw_name, mocker):
    # Mock detect_os 函数返回不同的操作系统名称
    mocker.patch('vault_warden_cli_tools.detect_os', return_value=os_name)

    # 获取 BW 工具路径
    bw_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bw_cli")
    bw_name = expected_bw_name

    # BW 工具完整地址路径
    bw_tool = download_bw_tool(bw_path=bw_path, bw_name=bw_name)

    assert os.path.exists(bw_tool) is True
