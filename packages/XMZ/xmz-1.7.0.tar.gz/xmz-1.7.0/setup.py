from setuptools import setup

setup(
    name="XMZ",
    version="1.7.0",
    description="米粥SDK",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="祁筱欣",
    author_email="mzapi@x.mizhoubaobei.top",
    url="https://github.com/xiaomizhoubaobei/XMZAPI",  # 正确的 URL
    packages=["HWNLP"],
    install_requires=["huaweicloudsdkcore", "huaweicloudsdknlp"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
