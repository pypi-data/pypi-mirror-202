# data2vec

data2Vec是一个Python工具，用于数据向量表征。

它可以将任何形式的数据转换为向量矩阵，并能够将这些向量存储在向量数据库中以供后续使用。

使用data2Vec，您可以轻松地处理各种数据类型，如文本、图像、音频等，并将其转换为向量表示形式，以便于特征提取、相似度计算、聚类等任务

## 安装

```
pip install data2Vec
```

## 使用

```python
from data2vec import Img2Vec

# img2vec = Img2Vec()
# 向量数据 单个
# vec = img2vec.get_vec('../data/cat.0.jpg')
# print(vec)

# 向量数据 多个
# vec = img2vec.get_list_vec('../data')
# print(vec)

```

## 支持模型

| Model name | Return vector length |
|------------|----------------------|
| Alexnet    | 1000                 |
| Resnet-18  | 1000                 |
| Resnet-34  | 1000                 |
| Resnet-50  | 1000                 |
| Resnet-101 | 1000                 |
| Resnet-152 | 1000                 |


## 例子

### 图像存储到[`pinecone`](https://www.pinecone.io/)向量数据库



```python
import pinecone
from data2vec import Img2Vec

# https://www.pinecone.io/

pinecone.init(api_key="xxx", environment="xxx")
img2vec = Img2Vec()
# 存储向量数据 单个
# vec = img2vec.get_vec('../data/cat.0.jpg')
# index = pinecone.Index("xxx")
# index.upsert(vec)
# fetch_response = index.fetch(ids=["cat.0.jpg"])
# print(fetch_response)

# 存储向量数据 多个
# vec = img2vec.get_list_vec('../data')
# index = pinecone.Index("xxx")
# index.upsert(vec)
# fetch_response = index.fetch(ids=["cat.0.jpg"])
# print(fetch_response)

# 相似度查询
index = pinecone.Index("xxx")
vec = img2vec.get_vec('../data/cat.0.jpg')
r = index.query(
    vector=vec[0][1],
    top_k=5,
)
print(r)
"""
Using cuda device
resnet18 model loaded
{'matches': [{'id': 'cat.0.jpg', 'score': 1.0, 'values': []},
             {'id': 'cat.7.jpg', 'score': 0.70519489, 'values': []},
             {'id': 'cat.20.jpg', 'score': 0.696186125, 'values': []},
             {'id': 'cat.14.jpg', 'score': 0.691424072, 'values': []},
             {'id': 'cat.8.jpg', 'score': 0.686835527, 'values': []}],
 'namespace': ''}
 
"""