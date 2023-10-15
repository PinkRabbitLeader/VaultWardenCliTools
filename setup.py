from setuptools import setup, find_packages

with open("./VaultWardenApi/__init__.py") as f:
    for line in f.readlines():
        if line.startswith("version"):
            delim = '"' if '"' in line else "'"
            version = line.split(delim)[1]
            break
    else:
        print("Can't find version! Stop Here!")
        exit(1)

with open('README.md', encoding='UTF-8') as f:
    long_description = f.read()

setup(
    name='VaultWardenApi',
    version=version,
    url='https://github.com/PinkRabbitLeader/VaultWardenApi',
    license='MIT',
    author='lzb',
    author_email='1072095696@qq.com',
    description="为自建VaultWarden服务提供接口封装服务。"
                "Provide interface encapsulation services for self-built VaultWarden services.",
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
        "Source": "https://github.com/PinkRabbitLeader/VaultWardenApi",
        "Tracker": "https://github.com/PinkRabbitLeader/VaultWardenApi/issues",
    },
    python_requires='>=3.6',
    packages=find_packages(where=".", exclude=['test*']),
)