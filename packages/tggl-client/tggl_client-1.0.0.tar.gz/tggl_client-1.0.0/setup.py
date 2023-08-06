from setuptools import setup, find_packages

setup(
    name='tggl_client',
    version='1.0.0',
    description='Tggl python client',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    keywords=['Tggl', 'feature flag'],
)