from setuptools import setup, find_packages

requirements = [
    'setuptools',
    'numpy',
    'requests',
    'opencv-python',
    'pillow',
    'torch',
    'groundingdino',
    'torchvision',
    'pyyaml',
    'transformers',
    'addict',
    'yapf',
    'supervision',
    'matplotlib',
    'pycocotools',
    'timm'
]

__version__ = 'V3.04.12'

setup(
    name='meta-label',
    version=__version__,
    author='CachCheng',
    author_email='tkggpdc2007@163.com',
    url='https://github.com/CachCheng/cvlabel',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    description='Meta Auto Label Toolkit',
    license='Apache-2.0',
    packages=find_packages(exclude=('docs', 'tests', 'scripts')),
    zip_safe=True,
    include_package_data=True,
    install_requires=requirements,
)
