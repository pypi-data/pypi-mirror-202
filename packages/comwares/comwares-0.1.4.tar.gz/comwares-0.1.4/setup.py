# setup.py

from setuptools import setup, find_packages

setup(
    name="comwares",
    version="0.1.4",
    author="Kevin Zhu",
    description="This project provides middlewares for a startup company.",
    packages=find_packages(),
    install_requires=[
        'tencentcloud_sdk_python',
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
        'requests',
        'retry',
        'setuptools',
        'SQLAlchemy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
