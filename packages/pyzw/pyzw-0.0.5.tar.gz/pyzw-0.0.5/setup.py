#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup

# 读取指定文件内容
def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pyzw',
    version='0.0.5',
    author='XueLiren',
    author_email='liren1029@gmail.com',
    maintainer='XueLiren',
    maintainer_email='liren1029@gmail.com',
    license='Apache Software License 2.0',
    keywords="中文编程 ",
    url='https://github.com/XueLiren/PyZW',
    description='Python中文库（PyZW）是基于Python标准库和诸多第三方库再次封装的中文模块，其函数命令超过1000个，涵盖了人工智能、键鼠操作、找图找色、'
                '网页自动化、手机自动化、OCR、YOLO、OpenCV、Word文档、Excel表格、PPT演示等多个领域。封装目的仅仅是为了将英文内容翻译成中文，'
                '从而使得生活、工作语言是中文的人群也能很好地学习、使用Python，享受编程带来的便利与乐趣！',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    packages=['pyzw'],
    python_requires='>=3.5',
    install_requires=[''],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],

)
