from setuptools import setup, find_packages

setup(
    name='financial_metrix_by_podpivas',
    version='0.1',
    packages=find_packages(),
    description='A package for calculating net profit and ROI',
    author='podpivas',
    author_email='k.shaykhraziev@edu.centraluniversity.ru',
    install_requires=[
        'setuptools',
    ],
    entry_points={
        'console_scripts': [
            'finance-calc=main:main',  # Добавляем команду для запуска
        ],
    },
)
