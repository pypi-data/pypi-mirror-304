import os
from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = os.getenv("CI_COMMIT_TAG", "0.0.0")

setup(
    name="fmo-cli",
    version=VERSION,
    author="Gudjon Magnusson",
    author_email="gmagnusson@fraunhofer.org",
    description="Command Line Interface to access and upload FindMyOyster data",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["fmo", "fmo.cli", "fmo.draw", "fmo.simulate"],
    keywords=["FindMyOyster", "CLI"],
    python_requires=">=3.7, <4",
    install_requires=[
        "click>=8.0.0",
        "pandas>=2.0.0",
        "requests>=2.28.2",
        "python_dotenv>=1.0.0",
        "geojson>=3.0.1",
    ],
    entry_points={
        "console_scripts": [
            "fmo=fmo.cli:invoke_cli",
        ]
    },
)
