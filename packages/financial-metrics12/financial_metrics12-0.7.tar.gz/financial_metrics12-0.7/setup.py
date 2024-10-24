from setuptools import setup, find_packages

setup(
    name='financial_metrics12',
    version='0.7',
    description='Package for calculating net profit and ROI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Nikita1207',
    author_email='dorogin345@gmail.com',
    url='',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={
        'console_scripts': [
            'financial_metrics1=financial_metrics1:main',
        ],
    },
)