from setuptools import setup, find_packages

setup(
    name='pycanpool',
    version='0.0.2',
    author='maminjie',
    author_email='canpool@163.com',
    description='A simple fancy package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://gitee.com/icanpool/pycanpool",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
