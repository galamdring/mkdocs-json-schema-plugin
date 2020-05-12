# -*- coding: utf-8 -*-
from setuptools import setup

with open("README.md") as f:
    readme = f.read()

setup(
    name="MkDocsJsonSchemaPlugin",
    version="0.0.1",
    description="MkDocs Plugin to parse json schemas.",
    long_description=readme,
    keywords=["mkdocs", "plugin", "json", "schema"],
    author="Luke McKechnie",
    author_email="galamdring@gmail.com",
    url="https://github.com/galamdring/mkdocs-json-schema-plugin",
    license="MIT license",
    packages=["mkdocs_json_schema_plugin"],
    install_requires=["mkdocs", "webpreview>=1.6.0"],
    python_requires=">=3.4, <4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    # This entry point is necessary for MkDocs to be able to use the plugin
    entry_points={
        'mkdocs.plugins': [
            'json-schema = mkdocs_json_schema_plugin.jsonschema:JsonSchema',
        ]
    },
)
