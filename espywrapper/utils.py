import os

from .__version__ import getVersion

PKG_VERSION = getVersion()
UA = f'espywrapper/{PKG_VERSION}'

def getCredentials():
    email = os.environ.get('ES_URL')
    password = os.environ.get('ES_APIKEY')

    if email and password:
        return (email, password)
    else:
        return (None , None)