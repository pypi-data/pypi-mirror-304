import pandas as pd
import requests
import logging


class WDCClient: 

    def __init__(self, host: str, token = None):
        self.logger = logging.getLogger(__name__)
        self.host = host 
        self.token = token
        
        self.session = requests.Session()
        if self.token != None: 
            self.session.headers.update({'token': self.token})

        
    def loadAsDataFrame(self, endpoint: str) -> pd.DataFrame: 
        json = self.loadAsJson(endpoint);
        
        return pd.json_normalize(json)
        
        
    def loadAsJson(self, endpoint: str) -> []: 
        res = []
        url = self.host + "/" + endpoint
        
        while url != None: 
            response = self.session.get(url)
            self.logger.debug("headers: %s", response.headers)
    
            json = response.json()
            
            res.extend(json["content"])
            
            # gehts weiter?
            if 'links' in json and 'next' in json['links']:
                url = json['links']['next']
                self.logger.debug("nextLink %s", next)
            else: 
                url = None
        
        return res
