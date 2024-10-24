"""
Project setup file
"""
import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='sageintacctsdkDIOB',
    version='1.1.1',
    author='Ashwin T, Mustafah',
    author_email='ashwin.t@fyle.in, m.poonjany@decisioninc.com',
    description='Python SDK for accessing Sage Intacct APIs',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['sage-intacct', 'sage', 'fyle', 'api', 'python', 'sdk'],
    url='https://github.com/fylein/sageintacct-sdk-py',
    packages=setuptools.find_packages(),
    install_requires=['requests>=2.25.0', 'xmltodict==0.12.0'],
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
