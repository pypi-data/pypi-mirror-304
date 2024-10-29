# setup.py

from setuptools import setup, find_packages

setup(
    name='sage_core',
    version='0.1.1-alpha',  # Обновленная версия с пометкой "alpha"
    author='Ваше Имя',
    author_email='your.email@example.com',
    description='SAGE Core - универсальный движок для взаимодействия между плагинами.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/sage_core',  # Замените на URL вашего репозитория
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Указание на альфа-версию
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
