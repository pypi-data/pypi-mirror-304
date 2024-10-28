from setuptools import setup, find_packages

setup(
   name='task_1_something_something',
   version='0.1.1',
   packages=find_packages(),
    entry_points={
        'console_scripts': [
            'my-script=my_package.module:main_function',
        ],
    },
)
