# 说明：setuptools的构建脚本。它告诉setuptools你的包（例如名称和版本）以及要包含的代码文件。
# 时间：2023/4/12 09:46
# 作者：孔令辉
# 环境：Python v3.9.16、PaddlePaddle v2.4.1、PaddleNLP v2.4

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-kingkong",
    version="0.0.1",
    author="KingKong0318",
    author_email="konglinghui0318@126.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)