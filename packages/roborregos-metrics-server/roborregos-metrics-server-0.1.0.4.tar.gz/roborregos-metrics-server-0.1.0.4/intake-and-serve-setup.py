from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='roborregos-metrics-server',
    version='0.1.0.4',
    packages=find_packages(),
    install_requires=[
        'requests',
        'fastapi',
        'pydantic',
        'uvicorn',
        'pymongo',
        'psutil'
    ],
    entry_points={
        'console_scripts': [
            'robometrics-server = robometrics.server.IntakeAndServe:main'
        ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown'
)
