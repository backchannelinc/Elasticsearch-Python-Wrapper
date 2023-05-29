import time
import json
import requests
import pandas as pd

from .utils import *

from elasticsearch import Elasticsearch, helpers

__version__ = '1.2.1'

class EsPyWrapperResult:
    def __init__(self, results: dict = None):
        self.results = results
        self.timing = results['timing']
        self.timing_started = results['timing']['started']
        self.timing_ended = results['timing']['ended']
        self.timing_duration = results['timing']['duration']
        self.took = self.timing_duration
        self.hits = results['hits']
        self.count = self.hits['count']
        self.index = results['index']
        self.query = results['query']
        self.query_type = results['query_type']

    def dict(self):
        '''
        Returns a dictionary of the results.
        '''
        if self.query_type == 'sql':
            return self.df().to_dict('records')
        else:
            return self.hits['hits']

    
    def json(self):
        '''
        Returns a JSON string of the results.
        '''
        return json.dumps(self.dict())

    def df(self):
        '''
        Returns a Pandas DataFrame of the results.
        '''
        if self.query_type == 'sql':
            return pd.DataFrame(self.hits['hits']['rows'],columns=[x['name'] for x in self.hits['hits']['columns']])
        else:
            return pd.json_normalize(self.dict())
        
    def csv(self):
        '''
        Returns a CSV string of the results.
        '''
        return self.df().to_csv(index=False)

class EsPyWrapper:
    PACKAGE_VERSION = None
    USER_AGENT = None

    ES_URL, ES_APIKEY = '', ''

    ES_HEADERS = None

    ES_CONNECTION = None
    ES_SQL_CONNECTION = None

    RESULTS_CONTAINER = None
    DATAFRAME_CONTAINER = None

    def __init__(self):
        self.PACKAGE_VERSION = __version__
        self.USER_AGENT = f'espywrapper/{self.PACKAGE_VERSION}'
        
        self.ES_URL, self.ES_APIKEY = getCredentials()
        
        self.ES_HEADERS = {
            'Content-Type': 'application/json',
            'User-Agent': self.USER_AGENT
        }

        self.ES_CONNECTION = Elasticsearch(
            hosts=[f'{self.ES_URL}'],
            api_key=self.ES_APIKEY,
            headers=self.ES_HEADERS
        )

    def info(self):
        '''
        Returns information about the Elasticsearch instance.
        '''
        return self.ES_CONNECTION.info()

    def schema(self, index: str = '*'):
        '''
        Returns the schema of the index.
        '''
        return self.ES_CONNECTION.indices.get_mapping(index=index)
    
    def fields(self, index: str = '*'):
        '''
        Returns a list of fields in the index.
        '''
        schema = self.schema(index=index)
        return list(schema[list(schema.keys())[0]]['mappings']['properties'].keys())
    
    def indices(self):
        '''
        Returns a list of indices.
        '''
        return list(self.ES_CONNECTION.indices.get(index='*').keys())
    
    def index(self, index: str = '*'):
        '''
        Returns info about an index.
        '''
        return self.ES_CONNECTION.indices.get(index=index)
    
    def query_es(self, index: str = None, query: dict = None):
        '''
        Returns the results of a query.
        '''
        if not index:
            raise ValueError('index is required')
        if not query:
            raise ValueError('query is required')
        
        time_started = time.time()

        scanner = helpers.scan(self.ES_CONNECTION,
            query=query,
            index=index,
            request_timeout=300                       
        )

        time_ended = time.time()
        duration = time_ended - time_started

        results = []

        for document in scanner:
            results.append(document['_source'])

        return EsPyWrapperResult({
            'timing':{
                'started':time_started,
                'ended':time_ended,
                'duration':duration
            },
            'hits': {
                'hits': results,
                'count':len(results),
            },
            'took': duration,
            'index':index,
            'query':query,
            'query_type':'es'
        })
    
    def query_lucene(self, index: str = None, query: str = None):
        '''
        Returns the results of a Lucene query.
        '''
        if not index:
            raise ValueError('index is required')
        if not query:
            raise ValueError('query is required')
        
        body = {
            'query': {
                'query_string': {
                    'query': query
                }
            }
        }

        return self.query_es(index=index, query=body)
    
    def query_sql(self, query: str = None):
        '''
        Returns the results of a SQL query.
        '''
        if not query:
            raise ValueError('query is required')
        
        params = {
            'format': 'json'
        }

        body = {
            'query': query
        }

        ES_SQL_URL = self.ES_URL+'/_sql'

        authorized_headers = self.ES_HEADERS
        authorized_headers.update({'Authorization': f'ApiKey {self.ES_APIKEY}'})

        time_started = time.time()
        r = requests.post(ES_SQL_URL,headers=authorized_headers,params=params,json=body)

        if r.status_code != 200:
            raise Exception(r.json())

        results = r.json()
        
        if 'cursor' in list(results.keys()):
            cursor = results['cursor']
            while cursor:
                r = requests.post(
                    ES_SQL_URL,
                    headers=authorized_headers,
                    params=params,
                    json={'cursor': cursor}
                )
                results['rows'] += r.json()['rows']
                if 'cursor' in list(r.json().keys()):
                    cursor = r.json()['cursor']
                else:
                    cursor = None

        time_ended = time.time()
        duration = time_ended - time_started

        return EsPyWrapperResult({
            'timing':{
                'started':time_started,
                'ended':time_ended,
                'duration':duration
            },
            'hits': {
                'hits': results,
                'count':len(results),
            },
            'took': duration,
            'index':None,
            'query':query,
            'query_type':'sql'
        })