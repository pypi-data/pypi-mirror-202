from setuptools import setup, find_namespace_packages

setup(
    name='lottery_generator',
    version='1.1.0',
    description='very helpful lottery',
    url='https://github.com/VadimTrubay/lottery_generator.git',
    author='Trubay_Vadim',
    author_email='vadnetvadnet@ukr.net',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    install_requires=['colorama'],
    entry_points={'console_scripts': ['lottery_generator=lottery_generator.main:main']}
)