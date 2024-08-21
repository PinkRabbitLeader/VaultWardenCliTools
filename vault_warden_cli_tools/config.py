import os


class Config:
    def __init__(self, env_file=None):
        # 加载.env文件（如果提供了）
        if env_file:
            from dotenv import load_dotenv
            load_dotenv(env_file, override=True)

        # 从环境变量中读取配置项
        self.bw_client_id = os.getenv('BW_CLIENTID')
        self.bw_client_secret = os.getenv('BW_CLIENTSECRET')
        self.bw_account = os.getenv('BW_ACCOUNT')
        self.bw_password = os.getenv('BW_PASSWORD')
        self.bw_server = os.getenv('BW_SERVER', 'https://vault.bitwarden.com')
        self.bw_timeout = int(os.getenv('BW_TIMEOUT', 20))
        self.appdata_dir = os.getenv('BITWARDENCLI_APPDATA_DIR')

        # 如果appdata_dir没有设置，下载BW工具
        if not self.appdata_dir:
            self._download_bw_tool()

    def _download_bw_tool(self):
        """下载BW工具并设置appdata_dir"""
        from vault_warden_cli_tools import download_bw_tool
        download_bw_tool()  # 调用外部函数下载工具

        # 更新appdata_dir环境变量
        self.appdata_dir = os.getenv('BITWARDENCLI_APPDATA_DIR')
        if not self.appdata_dir:
            raise RuntimeError("BW工具下载失败，未能设置BITWARDENCLI_APPDATA_DIR环境变量")

    def __repr__(self):
        return f"Config(bw_server={self.bw_server}, appdata_dir={self.appdata_dir}, timeout={self.bw_timeout})"

    def __str__(self):
        """提供类的字符串表示，便于调试"""
        return (
            f"Bitwarden Config:\n"
            f"Server: {self.bw_server}\n"
            f"Timeout: {self.bw_timeout}\n"
            f"App Data Directory: {'已设置' if self.appdata_dir else '未设置'}\n"
            f"Client ID: {'已设置' if self.bw_client_id else '未设置'}\n"
            f"Client Secret: {'已设置' if self.bw_client_secret else '未设置'}\n"
            f"Account: {'已设置' if self.bw_account else '未设置'}"
        )
