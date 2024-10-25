from setuptools import setup, find_packages
import os


def find_pyc_files():
    pyc_files = []
    for root, dirs, files in os.walk('discordpy_common'):
        for file in files:
            if file.endswith('.pyc'):
                pyc_files.append(os.path.join(root, file))
    return pyc_files


setup(
    name='discordpy-common',
    version='0.2.1',
    packages=find_packages(include=['discordpy_common', 'discordpy_common.*']),
    data_files=[('discordpy_common', find_pyc_files())],
    include_package_data=True,
    install_requires=[
        'discord.py',
        'motor',
        'pymongo',
    ],
    python_requires='>=3.12',
    author='pyPoul',
    license='MIT',
    description='Common tools for discord.py bots',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pyPoul/discordpy-common',
)
