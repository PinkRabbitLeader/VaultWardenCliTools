__all__ = ["download_bw_tool", "update_bw"]

import os
import zipfile

import requests

from vault_warden_cli_tools.exceptions import DownloadError
from vault_warden_cli_tools.utils import detect_os, extract_date


def download_bw_tool(bw_path: str, bw_name: str) -> str:
    print("开始下载 BW 终端管理工具")
    os.makedirs(bw_path, exist_ok=True)
    _bw = os.path.join(bw_path, bw_name)
    system = bw_name.split('_')[1].replace('.exe', '')
    url = f"https://vault.bitwarden.com/download/?app=cli&platform={system}"
    response = requests.get(url)
    if response.status_code == 200:
        # 获取文件名
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            file_name = content_disposition.split('filename=')[1]
        else:
            file_name = os.path.basename(url)

        # 拼接ZIP文件路径并保存ZIP文件
        zip_file_path = os.path.join(bw_path, file_name)

        with open(zip_file_path, 'wb') as file:
            file.write(response.content)

        # 解压ZIP文件
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                if "bw" in member:
                    with zip_ref.open(member) as source, open(_bw, 'wb') as target:
                        target.write(source.read())
                    break

        # 删除ZIP文件
        # os.remove(zip_file_path)
        print("BW 终端管理工具下载成功")
        return _bw
    else:
        raise DownloadError(f'BW 工具下载失败, 原错误：{response.content.decode("utf-8")}')


def update_bw() -> None:
    print("开始更新 BW 终端管理工具")
    os_name = detect_os()
    if os.path.exists(
            _bw_whole_path := os.path.join(
                (_bw_path := os.path.dirname(os.path.abspath(__file__))),
                (_bw_name := (f"bw_windows.exe" if os_name == "windows" else f"bw_{os_name}"))
            )
    ):
        matching_files = [
            filename for filename in os.listdir(os.path.dirname(os.path.abspath(__file__)))
            if filename.startswith(f"bw-{os_name}")
        ]
        latest_file = max(matching_files, key=extract_date)
        url = f"https://vault.bitwarden.com/download/?app=cli&platform={os_name}"
        response = requests.get(url)
        if response.status_code == 200:
            # 获取文件名
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition:
                file_name = content_disposition.split('filename=')[1]
            else:
                file_name = os.path.basename(url)
            if latest_file != file_name:
                os.remove(os.path.join(_bw_path, latest_file))
                os.remove(_bw_whole_path)
                _bw = download_bw_tool(bw_name=_bw_name, bw_path=_bw_path)
        else:
            raise DownloadError(f'BW 工具下载失败，更新失败，原错误：{response.content.decode("utf-8")}')

    print("更新 BW 终端管理工具结束")
