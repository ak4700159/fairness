## setup.py
from glob import glob
from os.path import basename, splitext
from setuptools import find_packages, setup

setup(
    name='fair', # 패키지명
    version='0.0.1', # 패키지 버전
    packages=find_packages(where='setting'), # 패키지 위치
    package_dir={'': 'setting'},
    install_requires=[
        "selenium==4.34.2", 
        "newspaper3k==0.2.8", 
        "pymysql==1.1.1",
        "seaborn==0.13.2", 
        "matplotlib==3.10.3", 
        "openapi==2.0.0", 
        "langchain==0.3.26", 
        "langchain-teddynote==0.3.45"],
    python_requires=">=3.12.0",
    py_modules=[splitext(basename(path))[0] for path in glob('setting/*.py')],
)

