from espywrapper import EsPyWrapper

esx = EsPyWrapper()

INDEX = 'test-*'
LUCENE_QUERY = 'yay'

results = esx.query_lucene(INDEX, LUCENE_QUERY)

# print python dict
print(results.dict())

# print json
print(results.json())

# print pandas dataframe
print(results.df())