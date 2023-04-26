import os
import pandas as pd

def getCredentials():
    email = os.environ.get('ES_URL')
    password = os.environ.get('ES_APIKEY')

    if email and password:
        return (email, password)
    else:
        return (None , None)
    
def resultsToDataFrame(results):
    return pd.DataFrame(results[1], columns=results[0])