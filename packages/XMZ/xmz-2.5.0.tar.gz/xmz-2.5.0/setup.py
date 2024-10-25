# from setuptools import setup, find_packages
#
#
# setup(
#     name="XMZ",
#     version="2.3.0",
#     description="米粥SDK",
#     long_description=open("README.md", encoding="utf-8").read(),
#     long_description_content_type="text/markdown",
#     author="祁筱欣",
#     author_email="mzapi@x.mizhoubaobei.top",
#     url="https://github.com/xiaomizhoubaobei/XMZAPI",
#     packages=find_packages(),
#     install_requires=["huaweicloudsdkcore", "huaweicloudsdknlp"],
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
# )
from setuptools import setup, find_packages

setup(
    name="XMZ",
    version="2.5.0",
    description="米粥SDK",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="祁筱欣",
    author_email="mzapi@x.mizhoubaobei.top",
    url="https://github.com/xiaomizhoubaobei/XMZAPI",
    packages=("XMZAPI", "XMZAPI.HWNLP"),
    install_requires=["huaweicloudsdkcore", "huaweicloudsdknlp"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
