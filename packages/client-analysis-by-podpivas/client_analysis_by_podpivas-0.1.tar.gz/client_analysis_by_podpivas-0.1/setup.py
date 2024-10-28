from setuptools import setup, find_packages

setup(
    name='client_analysis_by_podpivas',
    version='0.1',
    author='podpivas',
    author_email='k.shaykhraziev@edu.centraluniversity.ru',
    description='Анализ данных о клиентах',
    long_description_content_type='text/markdown',
    packages=find_packages(include=['client_analysis', 'client_analysis.*']),
    install_requires=[
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'client-analysis=main:main',
        ],
    },
    py_modules=['main'],  # Добавляем main как модуль
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # или другая лицензия
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
