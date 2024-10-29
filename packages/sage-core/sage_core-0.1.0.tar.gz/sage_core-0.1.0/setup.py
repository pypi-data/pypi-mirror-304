# setup.py

from setuptools import setup, find_packages

setup(
    name='sage_core',
    version='0.1.0',
    author='AGStudios',
    author_email='amckinatorgames@gmail.com',
    description='SAGE Core - универсальный движок для взаимодействия между плагинами.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/sage_core',  # Замените на URL вашего репозитория
    packages=find_packages(),
    install_requires=[
        # Добавьте необходимые зависимости, если они есть
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Замените на вашу лицензию
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
