from setuptools import setup, find_packages

setup(
    name="context_collector",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'context-collector=context_collector',
        ],
    },
)