from setuptools import setup, find_packages

with open('README.md', encoding='UTF-8') as f:
    long_description = f.read()

setup(
    name='vault_warden_cli_tools',
    version='0.0.1',
    url='https://github.com/PinkRabbitLeader/VaultWardenCliTools',
    license='MIT',
    author='lzb',
    author_email='1072095696@qq.com',
    description="基于 Bitwarden CLI 工具(`bw`) 封装的 Python 包，为 Vault Warden 提供命令行接口工具。"
                "A Python package that wraps the Bit Warden CLI tool (`bw`) to provide cli tools for Vault Warden.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    project_urls={
        "Source": "https://github.com/PinkRabbitLeader/VaultWardenCliTools",
        "Tracker": "https://github.com/PinkRabbitLeader/VaultWardenCliTools/issues",
    },
    python_requires='>=3.6',
    packages=find_packages(where=".", exclude=['test*']),
)
