from setuptools import setup, find_packages

setup(
    name='for_task_1',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'for_task_1=for_task_1.__main__:main',
        ],
    },
)
