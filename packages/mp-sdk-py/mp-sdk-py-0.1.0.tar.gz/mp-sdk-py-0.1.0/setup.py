from setuptools import setup, find_packages

setup(
    name="mp-sdk-py",                # 项目名称
    version="0.1.0",             # 版本号
    author="bp developer",          # 作者
    description="framework for monitor development", # 简短描述
    packages=find_packages(where="src"),  # 自动找到所有包
    package_dir={"": "src"},     # 指定包的根目录
    install_requires=[           # 项目依赖
        "pytest-playwright>=0.5.2",
        "websockets>=13.1"
    ],
    python_requires=">=3.9"
)