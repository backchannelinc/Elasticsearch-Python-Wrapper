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