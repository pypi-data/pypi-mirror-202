from pathlib import Path

from setuptools import find_packages, setup

setup(
    name='VideoPro10',
    version=1.0,
    description='Este pacote irá fornecer ferramentas de processamento de video',
    long_description=Path('README.md').read_text(),
    author='Paulo Ribas',
    author_email='paulo-ribas@live.com',
    keywords=['camera', 'video', 'processamento'],
    packages=find_packages()
)
