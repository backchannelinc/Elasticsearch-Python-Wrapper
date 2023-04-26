# Elasticsearch-Python-Wrapper
Python package for querying Elasticsearch databases, optimized for SQL querying and dataframe usage.

Getting started is as easy as:
```
from espywrapper import EsPyWrapper

esx = EsPyWrapper()

SQL_QUERY = '''select
    *
    from "test-*"
'''

results = esx.query_sql(SQL_QUERY)
```

The `results` object can transform into JSON, Python dictionary, a Pandas dataframe, or a CSV.

Requires the following environment variables:
- `ES_URL`: The hostname of the Elasticsearch server. Include the protocol and port.
- `ES_APIKEY`: An API key from the Elasticsearch server.