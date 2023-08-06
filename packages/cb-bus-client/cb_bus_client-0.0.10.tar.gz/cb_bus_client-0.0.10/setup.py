from setuptools import setup

setup(
    name="cb_bus_client",
    version="0.0.10",
    packages=["cb_bus_client"],
    package_data={"*": ["*.txt", "*.md"]},
    include_package_data=True,
    install_requires=["mycroft-messagebus-client==0.9.1", "pyxdg", "combo_lock>=0.1.1"],
    url="https://github.com/HelloChatterbox/chatterbox-bus-client",
    license="Apache-2.0",
    author="Kevin Elgan",
    author_email="kevin@hellochatterbox.com",
    description="Chatterbox Messagebus Client",
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
