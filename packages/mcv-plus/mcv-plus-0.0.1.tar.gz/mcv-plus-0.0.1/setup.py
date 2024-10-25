from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

setup(
    name="mcv-plus",
    version="0.0.1",
    description="Opencv图像处理增强库",
    author="KateTseng",
    author_email="Kate.TsengK@outlook.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="Auto Script Testing",
    project_urls={},
    packages=find_packages(),
    include_package_data=True,
    package_data={},
    install_requires=["pillow",
                      'opencv-python',
                      'numpy'
                      ],
    python_requires=">=3",
)