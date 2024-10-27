from setuptools import setup, find_packages

setup(
    name='receipt_generator',
    version='0.1.1',
    description='Пакет для автоматической генерации чеков на основе заказов',
    author='Nikita',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'generate-receipt = receipt_generator.cli:main',
        ],
    },
)
