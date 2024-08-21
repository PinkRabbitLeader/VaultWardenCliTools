__all__ = ["download_bw_tool", "update_bw"]

import os
import zipfile

import requests

from vault_warden_cli_tools.exceptions import DownloadError
from vault_warden_cli_tools.utils import detect_os, extract_date


def download_bw_tool() -> None:
    from tqdm import tqdm
    # 获取 BW 工具
    os_name = detect_os()  # 获取当前操作系统名称
    bw_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bw_cli")
    bw_name = f"bw_windows.exe" if os_name == "windows" else f"bw_{os_name}"
    _bw = os.path.join(bw_path, bw_name)
    if not (os.path.exists(bw_path) and os.path.exists(_bw)):
        os.makedirs(bw_path, exist_ok=True)
        url = f"https://vault.bitwarden.com/download/?app=cli&platform={os_name}"
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # 获取文件总大小（字节数）
            total_size = int(response.headers.get('content-length', 0))
            # 设置块大小（以字节为单位）
            block_size = 1024
            # 获取文件名
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition:
                file_name = content_disposition.split('filename=')[1]
            else:
                file_name = os.path.basename(url)

            # 拼接ZIP文件路径并保存ZIP文件
            zip_file_path = os.path.join(bw_path, file_name)

            print("开始下载 BW 终端管理工具")
            try:
                # 打开文件准备写入
                with open(zip_file_path, 'wb') as file:
                    # 使用 tqdm 显示进度条
                    with tqdm(total=total_size, unit='B', unit_scale=True, desc=file_name) as progress_bar:
                        for data in response.iter_content(block_size):
                            # 写入下载的数据块
                            file.write(data)
                            # 更新进度条
                            progress_bar.update(len(data))
            except (requests.exceptions.RequestException, KeyboardInterrupt) as e:
                # 如果下载过程中发生异常，删除未完成的文件
                if os.path.exists(zip_file_path):
                    os.remove(zip_file_path)
                raise DownloadError(f"下载过程中出错: {e}")

            # 解压ZIP文件
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    if "bw" in member:
                        with zip_ref.open(member) as source, open(_bw, 'wb') as target:
                            target.write(source.read())
                        break

            print("BW 终端管理工具下载成功")
        else:
            raise DownloadError(f'BW 工具下载失败, 原错误：{response.content.decode("utf-8")}')

    os.environ['BITWARDENCLI_APPDATA_DIR'] = bw_path


def update_bw() -> None:
    print("开始更新 BW 终端管理工具")
    os_name = detect_os()
    if os.path.exists(
            _bw_whole_path := os.path.join(
                (_bw_path := os.path.join(os.path.dirname(os.path.abspath(__file__)), "bw_cli")),
                (_bw_name := (f"bw_windows.exe" if os_name == "windows" else f"bw_{os_name}"))
            )
    ):
        matching_files = [
            filename for filename in os.listdir(_bw_path)
            if filename.startswith(f"bw-{os_name}")
        ]
        # 获取最晚日期的bw工具压缩文件
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
                _bw = download_bw_tool()
        else:
            raise DownloadError(f'BW 工具下载失败，更新失败，原错误：{response.content.decode("utf-8")}')

    print("更新 BW 终端管理工具结束")
