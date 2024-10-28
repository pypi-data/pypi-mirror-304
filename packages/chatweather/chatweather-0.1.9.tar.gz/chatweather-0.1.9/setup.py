from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chatweather",
    version="0.1.9",
    author="SanghyunPark",
    author_email="hirvahapjh@gmail.com",
    description="A package for weather forecasting and ChatGPT integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daisybum/pyWeather",
    packages=find_packages(),
    include_package_data=True,
    package_data={'chatweather': ['config.py', 'config.yaml']},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests",
        "xmltodict",
        "openai==1.52.2",
        "pytest==8.3.3"
    ],
)