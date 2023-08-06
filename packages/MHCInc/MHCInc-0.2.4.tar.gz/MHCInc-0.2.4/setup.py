import setuptools

with open("README.rst", "r",encoding = "UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MHCInc",
    version="0.2.4",
    author="Mhc-inc",
    author_email="Wf6350177@163.com",
    description="改进漏洞：重复模块引用时无法配置删除的环境，使用MHCInc.module.setup()即可",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/MHCInc/",
    project_urls={
        "Bug Tracker": "https://github.com/Mhc-inc/MHCInc/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "MHCInc"},
    packages=setuptools.find_packages(where="MHCInc"),
    python_requires=">=3.9",
)
