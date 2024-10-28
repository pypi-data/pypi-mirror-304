from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="JunoAccessManager",  # 替换为你的项目名称
    version="1.0.1",  # 版本号
    author="Yuhui Wang",  # 作者姓名
    author_email="wangyuhui341@163.com",  # 作者邮箱
    description="Pulsar租户接入权限管理",  # 项目简介
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/your_project_name",  # 项目主页
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "annotated-types",
        "anyio",
        "bcrypt",
        "certifi",
        "cffi",
        "charset-normalizer",
        "click",
        "colorama",
        "cryptography",
        "ecdsa",
        "fastapi",
        "greenlet",
        "h11",
        "idna",
        "orjson",
        "passlib",
        "pyasn1",
        "pycparser",
        "pydantic",
        "pydantic-settings",
        "pydantic_core",
        "PyJWT",
        "PyMySQL",
        "python-decouple",
        "python-dotenv",
        "python-jose",
        "python-multipart",
        "requests",
        "rsa",
        "six",
        "sniffio",
        "SQLAlchemy",
        "SQLAlchemy-Utils",
        "starlette",
        "typing_extensions",
        "urllib3",
        "uvicorn",
    ],
    extras_require={
        "dev": ["pytest", "coverage"],
    },
)