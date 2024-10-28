from setuptools import setup, find_packages

setup(
    name='tsk_1',
    version='0.1.0',
    description='Пакет для расчета финансовых показателей',
    author='bardachell',
    author_email='jenda-penda@mail.ru',
    packages=find_packages(),
    install_requires=['argparse'],
    entry_points={
        'console_scripts': [
            'my_package = my_package.business_metrics:main',
        ],
    }
)
