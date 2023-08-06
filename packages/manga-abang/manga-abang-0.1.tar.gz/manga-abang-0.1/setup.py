'''
Author: AbangTan tan_yihan@housei-inc.com
Date: 2023-01-05 10:34:27
LastEditors: AbangTan tan_yihan@housei-inc.com
LastEditTime: 2023-04-14 17:49:11
FilePath: /manga-ocr/setup.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from pathlib import Path
from setuptools import setup

long_description = (Path(__file__).parent / "README.md").read_text('utf-8').split('# Installation')[0]

setup(
    name="manga-abang",
    version='0.1',
    description="OCR for Japanese manga",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AbangTanYiHan/manga_abang",
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=['manga_ocr'],
    include_package_data=True,
    install_requires=[
        "fire",
        "fugashi",
        "jaconv",
        "loguru",
        "numpy",
        "Pillow",
        "pyperclip",
        "sentencepiece",
        "torch>=1.0",
        "transformers>=4.12.5",
        "unidic_lite",
        "keyboard",
    ],
    entry_points={
        "console_scripts": [
            "manga_ocr=manga_ocr.__main__:main",
        ]
    },
)
