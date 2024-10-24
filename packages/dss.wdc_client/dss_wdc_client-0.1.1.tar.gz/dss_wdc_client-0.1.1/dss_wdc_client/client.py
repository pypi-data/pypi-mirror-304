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
        res = pd.DataFrame()
        url = self.host + "/" + endpoint
        
        while url != None: 
            response = self.session.get(url)
            self.logger.debug("headers: %s", response.headers)
    
            json = response.json()
            
            df = pd.json_normalize(json["content"])
            
            res = pd.concat([res, df])
            
            # gehts weiter?
            if 'links' in json and 'next' in json['links']:
                url = json['links']['next']
                self.logger.debug("nextLink %s", next)
            else: 
                url = None
            
        # index neu aufbauen
        res.reset_index(drop=True, inplace=True)
        
        return res
