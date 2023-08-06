import setuptools
import re

with open('VERSION') as f:
    version_str = f.read()


def get_version():
    # 从版本号字符串中提取三个数字并将它们转换为整数类型
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", version_str)
    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3))

    # 对三个数字进行加一操作
    patch += 1
    if patch > 9:
        patch = 0
        minor += 1
        if minor > 9:
            minor = 0
            major += 1
    new_version_str = f"{major}.{minor}.{patch}"
    return new_version_str


with open("README.md", "r") as fh:
    long_description = fh.read()
with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="yourtools",
    version=get_version(),
    author="zfang",
    author_email="founder517518@163.com",
    description="Python helper tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/yourtools/",
    packages=setuptools.find_packages(),
    data_files=["requirements.txt"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=required,
)


def write_now_version():
    print("Current VERSION:", get_version())
    with open("VERSION", "w") as version_f:
        version_f.write(get_version())


# 将新的版本号字符串回写入文件中
write_now_version()
