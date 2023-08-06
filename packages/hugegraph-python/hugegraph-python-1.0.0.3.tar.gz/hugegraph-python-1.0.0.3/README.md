# hugegraph-python
A Python SDK for Apache HugeGraph, maintained by [cvte research data-mining team](https://github.com/cvte-research-datamining/hugegraph-python).

This project currently in alpha testing, will open source the code soon.

#Installation
##PyPi
```
pip3 install gremlinapi

```
##Install from source
```
git clone git@github.com:gremlin/gremlin-python.git
cd gremlin-python
python3 setup.py install
```

#Examples
```python
from hugegraph import PyHugeGraph
# init client
client = PyHugeGraph("127.0.0.1", "8080", user="admin", pwd="pwd", graph="hugegraph")

# schema
schema = client.schema()
schema.getVertexLabels()

# graph
g = client.graph()
g.getVertexById("1:tom")
g.close()
```

Any questions contact [ming@apache.org](ming@apache.org)
