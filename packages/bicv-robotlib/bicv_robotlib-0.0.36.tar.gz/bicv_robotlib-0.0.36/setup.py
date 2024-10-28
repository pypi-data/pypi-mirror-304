from setuptools import setup, find_packages

setup(
    name='robotlib',
    version='0.0.1',
    author='toney_xzw',
    author_email='toney_xzw@126.com',
    description='BICV-AutoTestLib',
    packages=find_packages(),  # 自动查找并包含所有的包
    install_requires=[
        'requests',
        'numpy',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)