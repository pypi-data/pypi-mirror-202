from setuptools import setup, find_packages

setup(
    name='chronosTime',
    version='0.1.0',
    description='A library for measuring time elapsed',
    author='Chr0n0s',
    author_email='ch3guevara@proton.me',
    url='https://github.com/cybershinig4mi',
    packages=find_packages(),
    install_requires=[
        # list your dependencies here
        'numpy>=1.15.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
