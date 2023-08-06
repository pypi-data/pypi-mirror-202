from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='data2vec',
    version='0.0.3',
    keywords='Vector Pytorch Vector Database',
    description='data2Vec是一个Python工具，用于数据向量表征。',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT License',
    url='https://github.com/xuehangcang/data2vec',
    author='Xuehang Cang',
    author_email='xuehangcang@outlook.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'torch~=2.0.0',
        'torchaudio~=2.0.1',
        'torchvision~=0.15.1',
        "Pillow~=9.5.0",
        "tqdm~=4.65.0",
        "pinecone-client~=2.2.1",
    ],
)
