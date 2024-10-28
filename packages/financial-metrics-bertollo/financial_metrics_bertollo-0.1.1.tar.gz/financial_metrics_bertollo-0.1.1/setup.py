from setuptools import setup


setup(
    name='financial_metrics_bertollo',
    version='0.1.1',
    description='A package for calculating financial metrics such as net profit and ROI.',
    author='Victor Bertollo',
    author_email='bertollo.victor@gmail.com',
    packages=['financial_metrics'],
    entry_points={
        'console_scripts': [
            'financial_metrics=financial_metrics:main',
        ],
    },
    install_requires=[],
)
