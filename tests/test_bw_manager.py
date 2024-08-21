import os
import tempfile
from unittest.mock import patch, MagicMock

import pytest

from vault_warden_cli_tools import download_bw_tool


@pytest.fixture
def temp_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.mark.parametrize("os_name", ["windows", "linux", "macos"])
def test_download_bw_tool(os_name, mocker, temp_directory):
    bw_name = f"bw_windows.exe" if os_name == "windows" else f"bw_{os_name}"
    # Mock detect_os 函数返回不同的操作系统名称
    mocker.patch('vault_warden_cli_tools.bw_manager.detect_os', return_value=os_name)

    # Mock os.path.exists 来避免实际的文件系统检查
    mocker.patch('os.path.exists', return_value=False)

    # Mock os.makedirs 来避免实际的目录创建
    mocker.patch('os.makedirs')

    # Mock requests.get 来避免实际的网络请求
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {
        f'Content-Disposition': f'attachment; filename=bw-{os_name}-test.zip', 'content-length': '1024'
    }
    mock_response.iter_content = MagicMock(return_value=[b'data'] * 10)  # 模拟响应内容
    mock_get = mocker.patch('requests.get', return_value=mock_response)

    # Mock tqdm 来避免实际的进度条显示
    mocker.patch('tqdm.tqdm', lambda *args, **kwargs: MagicMock())

    # Mock zipfile.ZipFile 来避免实际的文件解压
    mock_zipfile = MagicMock()
    mock_zipfile.return_value.__enter__.return_value = mock_zipfile
    mock_zipfile.namelist.return_value = [bw_name]
    mock_zipfile.open.return_value.read.return_value = b'binary_data'
    mocker.patch('zipfile.ZipFile', mock_zipfile)

    # Mock open 来避免实际的文件写入
    mock_open = mocker.patch('builtins.open', mocker.mock_open())

    # 调用 download_bw_tool 函数，并传入临时目录
    with patch('vault_warden_cli_tools.bw_manager.os.path.dirname', return_value=temp_directory):
        download_bw_tool()

    # 验证结果
    assert os.getenv("BITWARDENCLI_APPDATA_DIR")

    # 验证 mock 方法被调用
    mock_open.assert_any_call(os.path.join(temp_directory, 'bw_cli', f'bw-{os_name}-test.zip'), 'wb')
    mock_open.assert_any_call(
        os.path.join(temp_directory, 'bw_cli', bw_name),
        'wb'
    )
    mock_zipfile.open.assert_called_once_with(bw_name)
    # 确保 requests.get 被调用了
    mock_get.assert_called_once_with(
        f"https://vault.bitwarden.com/download/?app=cli&platform={os_name}",
        stream=True
    )
