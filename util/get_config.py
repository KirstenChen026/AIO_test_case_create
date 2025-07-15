import json


class Jira_Config:

    def __init__(self) -> None:
        with open('data/jira_config.json') as f:
            self.config = json.load(f)
        
    def get_jira_url(self):

        return self.config['url']
    
    def get_aio_url(self):

        return self.config["AIO_BASE_URL"]

    def get_aio_token(self): 
        return self.config['AIOToken']   