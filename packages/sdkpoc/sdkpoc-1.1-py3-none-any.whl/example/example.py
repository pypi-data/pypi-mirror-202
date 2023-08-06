import requests

class MyapiExample:
    
    def __init__(self, client_id=None, token=""):
        self.client_id = client_id
        self.token = token
        self.content = 'application/json'
        self.header = "{}:{}".format(
                    self.client_id, self.token
                )
    def get_profile(self):
        url = "https://api.fyers.in/api/v2" + "/profile"
        response = requests.get(url=url, headers={"Authorization": self.header, 'Content-Type': self.content})
        return response 
