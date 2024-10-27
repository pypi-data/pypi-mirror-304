from setuptools import setup, find_packages

setup(
    name='CURoma-roi',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'my-script=roi.module:main_function',
        ],
    },
)
