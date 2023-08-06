from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='image_processing_by_cbcj',
    version='0.0.1',
    author='Cleber Bianchi',
    description='Image Precessing Package using skimage',
    long_description=page_description,
    long_description_content_type='text/markdown',
    url='https://github.com/CleberJesus/image_processing_package',
    packages=find_packages(),
    install_requires=requirements,
    python_required='>-3.5',
)