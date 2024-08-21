import os
from unittest.mock import patch, MagicMock

import pytest

from vault_warden_cli_tools import Config  # 假设你的类在 config.py 文件中


@pytest.fixture
def clear_env():
    """在每个测试前清除环境变量，确保测试环境一致"""
    os.environ.clear()


@pytest.fixture
def env_file(tmpdir):
    """创建一个临时的 .env 文件供测试使用"""
    d = tmpdir.mkdir("config")
    env_path = d.join("test.env")
    with open(env_path, 'w') as f:
        f.write("BW_CLIENTID=test_client_id\n")
        f.write("BW_CLIENTSECRET=test_client_secret\n")
        f.write("BW_ACCOUNT=test_account\n")
        f.write("BW_PASSWORD=test_password\n")
        f.write("BW_SERVER=https://test-server.com\n")
        f.write("BW_TIMEOUT=30\n")
        f.write("BITWARDENCLI_APPDATA_DIR=/mock/path/bw_cli\n")
    return str(env_path)


def test_config_initialization_with_env_file(clear_env, env_file):
    """测试通过 .env 文件初始化配置"""
    config = Config(env_file=env_file)
    assert config.bw_client_id == 'test_client_id'
    assert config.bw_client_secret == 'test_client_secret'
    assert config.bw_account == 'test_account'
    assert config.bw_password == 'test_password'
    assert config.bw_server == 'https://test-server.com'
    assert config.bw_timeout == 30
    assert config.appdata_dir == '/mock/path/bw_cli'


def test_config_manual_override(clear_env, env_file):
    """测试手动覆盖配置项"""
    config = Config(env_file=env_file)
    # 修改账号信息
    config.bw_account = 'manual_account'

    # 手动设置应覆盖从环境变量加载的值
    assert config.bw_client_id == 'test_client_id'
    assert config.bw_client_secret == 'test_client_secret'
    assert config.bw_account == 'manual_account'
    assert config.bw_password == 'test_password'
    assert config.bw_server == 'https://test-server.com'
    assert config.bw_timeout == 30
    assert config.appdata_dir == '/mock/path/bw_cli'


def test_config_with_partial_env_vars(clear_env):
    """测试只设置部分环境变量的情况"""
    with patch.dict(os.environ, {
        'BW_ACCOUNT': 'test_account',
        'BITWARDENCLI_APPDATA_DIR': '/mock/path/bw_cli'
    }):
        config = Config()
        assert config.bw_account == 'test_account'
        assert config.bw_client_id is None
        assert config.bw_client_secret is None


def test_download_bw_tool_called_if_no_appdata_dir(clear_env):
    """测试当appdata_dir未设置时，是否调用了下载BW工具的方法"""
    with patch('vault_warden_cli_tools.Config._download_bw_tool', MagicMock()) as mock_download_bw_tool:
        Config()
        mock_download_bw_tool.assert_called_once()


def test_appdata_dir_set_after_download(clear_env, mocker):
    """测试下载BW工具后appdata_dir是否设置正确"""
    mocker.patch('vault_warden_cli_tools.download_bw_tool', return_value=os.environ.update(
        {'BITWARDENCLI_APPDATA_DIR': '/mock/path/bw_cli'}
    ))
    config = Config()
    assert config.appdata_dir == '/mock/path/bw_cli'


def test_config_str_representation(clear_env):
    """测试Config类的字符串表示"""
    with patch.dict(os.environ, {
        'BW_CLIENTID': 'test_client_id',
        'BW_CLIENTSECRET': 'test_client_secret',
        'BW_SERVER': 'https://custom-server.com',
        'BITWARDENCLI_APPDATA_DIR': '/mock/path/bw_cli'
    }):
        config = Config()
        expected_str = (
            "Bitwarden Config:\n"
            "Server: https://custom-server.com\n"
            "Timeout: 20\n"
            "App Data Directory: 已设置\n"
            "Client ID: 已设置\n"
            "Client Secret: 已设置\n"
            "Account: 未设置"
        )
        assert str(config) == expected_str
