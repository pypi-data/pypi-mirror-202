# setup.py

from setuptools import setup, find_packages

setup(
    name="comwares",
    version="0.1.0",
    author="Kevin Zhu",
    packages=find_packages(),
    install_requires=[
        'cos_python_sdk_v5',
        'ffmpeg',
        'ffmpeg_python',
        'google_api_python_client',
        'google_auth_oauthlib',
        'matplotlib',
        'mplfinance',
        'numpy',
        'opencv_python',
        'pandas',
        'pdfplumber',
        'Pillow',
        'pymongo',
        'qcloud_cos',
        'requests',
        'retry',
        'setuptools',
        'SQLAlchemy',
        'tencentcloud_sdk_python',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
