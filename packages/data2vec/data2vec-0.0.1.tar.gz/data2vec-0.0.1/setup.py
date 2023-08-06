from setuptools import setup, find_packages

setup(
    name='data2vec',
    version='0.0.1',
    keywords='Vector Pytorch Vector Database',
    description='data2Vec是一种用于数据向量表征的工具，它将数据转换为向量矩阵并可以将其存储在向量数据库中。',
    license='MIT License',
    url='https://github.com/xuehangcang/data2vec',
    author='Xuehang Cang',
    author_email='xuehangcang@outlook.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'torch>=2.0.0',
        'torchaudio>=2.0.1',
        'torchvision>=0.15.1'
    ],
)
