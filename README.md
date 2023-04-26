# Elasticsearch-Python-Wrapper
The best way to query Elasticsearch with SQL.

Python package for querying Elasticsearch databases, optimized for SQL querying and dataframe usage.

Includes ability for scrolling through results over 10K (the Elasticsearch default).

Getting started is as easy as:
```
from espywrapper import EsPyWrapper

esx = EsPyWrapper()

SQL_QUERY = '''select
    *
    from "test-*"
'''

results = esx.query_sql(SQL_QUERY)

# print python dict
print(results.dict())

# print json
print(results.json())

# print pandas dataframe
print(results.df())

# print as csv
print(results.csv())
'''

results = esx.query_sql(SQL_QUERY)
```

The `results` object can transform into JSON, Python dictionary, a Pandas dataframe, or a CSV.

Requires the following environment variables:
- `ES_URL`: The hostname of the Elasticsearch server. Include the protocol and port.
- `ES_APIKEY`: An API key from the Elasticsearch server.